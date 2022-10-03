
from flask import Blueprint, request, jsonify
from . import utils

ranking_api = Blueprint('ranking_api', __name__)


@ranking_api.route('/api/ranked/new', methods = ['POST'])
def new_ranking():

    uid = utils.new(request.json['entries'])
    
    return(jsonify(
        body=f"New ranking tournament created: {uid}",
        uid=uid,
        )
    )

@ranking_api.route('/api/ranked/vote', methods = ['POST'])
def vote():
    uid = int(request.json['uid'])
    votes = request.json['votes']
    response = utils.vote(uid, votes)
    return(jsonify(
        body=response
    ))

@ranking_api.route('/api/ranked/get_candidates', methods = ['GET'])
def getCandidates():
    uid = int(request.args.to_dict()['uid'])
    response = utils.getCandidates(uid)
    return(jsonify(
        body=response
    ))

@ranking_api.route('/api/ranked/end', methods = ['GET'])
def endRound():
    uid = int(request.args.to_dict()['uid'])
    response = utils.endVoting(uid)
    return(jsonify(
        body=response
    ))