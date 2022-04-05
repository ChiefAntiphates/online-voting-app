from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv
import voting_utils as utils
import os
import redis

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

r = redis.Redis(host='localhost', port=6379)

socketio = SocketIO(
        app, 
        cors_allowed_origins=os.getenv('CLIENT_URL')or"http://localhost:3000",
        message_queue='redis://'
    )

button_clicks = 0



@app.route('/')
def hello_world():
    print("I got it!")
    r.publish("test1", "hello")
    return ("hello")

@app.route('/set_name')
def redis_set():
    args = request.args.to_dict()
    r.set('name', args['name'])
    return(f"Set name to {args['name']}.")

@app.route('/test')
def my_test():
    socketio.emit('test_topic', 'Success!!!', namespace='/testnp')
    return jsonify(body='This works!'), 200

@app.route('/click')
def click():
    global button_clicks
    button_clicks += 1
    socketio.emit('clicked', {"number": button_clicks}, namespace='/button_clicks')
    return jsonify(body="You clicked the button", clicks=button_clicks)

if __name__ == '__main__':
    app.debug=True
    socketio.run(
        app, host='0.0.0.0', port=os.getenv('SERVER_PORT') or 5000)