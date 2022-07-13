import json
from lib2to3 import refactor
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

from dotenv import load_dotenv
import os
import redis
import voting_utils

load_dotenv()

app = Flask(__name__)
#TODO: Restrict CORS to specific routes
CORS(app)

app.config['SECRET_KEY'] = 'secret!'

r = redis.Redis(host=os.getenv('REDIS_DOMAIN') or 'localhost', port=6379)

socketio = SocketIO(
        app, 
        cors_allowed_origins=os.getenv('CLIENT_URL') or 'http://localhost:3000',
        #message_queue='redis://' # << this breaks the server when a socketio connection is made...
    )


#TODO: Add route prefix '/api' programatically
#TODO: Check uid exists in many of the routes


@app.route('/api/new', methods = ['POST'])
def new_tournament():
    #TODO: Check that request body can be converted to JSON
    #TODO: Check that entries exists (maybe move into const)
    uid = voting_utils.new_tournament(r, request.json['entries'])
    matchups = voting_utils.generate_matchups(r, uid) #Generate first round of matchups
    
    return(jsonify(
        body=f"New tournament created: {uid}",
        uid=uid,
        matchups=matchups
        )
    )


@app.route('/api/current_round')
def get_current_round():
    #TODO: Check that uid exists
    current_round_ref = voting_utils.get_current_round(r, request.args.to_dict()['uid'])
    current_round_info = voting_utils.get_round_details(r, current_round_ref)
    total_votes = (sum([int(current_round_info[x]) for x in current_round_info.keys()]))
    return(jsonify(ref=current_round_ref, scores=current_round_info, votes=total_votes))



#TODO: Verify one vote per user (IP or cookies)
@app.route('/api/vote', methods = ['POST'])
def submit_vote():
    #TODO: Check that fields exist
    #TODO: Check that request body can be converted to JSON
    uid = request.json['uid']
    result = voting_utils.submit_vote(
        r, 
        uid, 
        request.json['round'], 
        request.json['vote']
    )
    if result[0]:
        socketio.emit('vote_cast', {"results": result[1]}, namespace=f'/{uid}')
        return(jsonify(result))
    else:
        return("Error!")

#TODO: Introduce automated round end timeouts
@app.route('/api/end_round')
def end_round():
    uid = request.args.to_dict()['uid']
    ref = request.args.to_dict()['ref']
    result = voting_utils.end_round(r, uid, ref)
    if not result[0]: # If round isn't active, return actual active round
        return jsonify(body=result[1], current_round=result[2])
    socketio.emit('round_end', {"results": result[1], "winner": {"overall": result[3], "name": result[2]}}, namespace=f'/{uid}')
    return(result[1])


@app.route('/api/candidates')
def get_candidates():
    uid = request.args.to_dict()['uid']
    candidates = voting_utils.get_candidates(r, uid)
    return jsonify(data=candidates)


@app.route('/api/results')
def get_results():
    uid = request.args.to_dict()['uid']
    results = voting_utils.get_results(r, uid)
    return jsonify(data=results)

@app.route('/api/is_active')
def is_active():
    active = voting_utils.check_if_active(r, request.args.to_dict()['uid'])
    return jsonify(active=active)
    

#Example Routes
@app.route('/')
def hello_world():
    print("I got it!")
    return ("hello")


if __name__ == '__main__':
    app.debug=True
    socketio.run(
        app, host='0.0.0.0', port=os.getenv('SERVER_PORT') or 5000)