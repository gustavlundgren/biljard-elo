from flask import Blueprint, jsonify, request
from server.src import db
from firebase_admin import auth
import datetime

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/api/games/get', methods=['GET'])
def get_games():
    docs = db.collection('games').get()
    return jsonify({'data': [doc.to_dict() for doc in docs]}), 200


@routes_blueprint.route('/api/games/add', methods=['POST'])
def add_game():
    data = request.json
    players = data.get('players')
    winner = data.get('winner')
    token = data.get('token')
    
    if not players or not winner:
        return jsonify({'error': 'Players and winner required'}), 400
    
    if winner not in players:
        return jsonify({'error': 'Winner must be one of the players in the game'}), 400
    
    if not token:
        return jsonify({'error': 'Please supply a token'})
    
    try:
        # Verify the toke from the user
        auth.verify_id_token(token)
        
        # Add the new game to the collection
        db.collection('games').add({
            'players': players, 
            'winner': winner, 
            'time': datetime.datetime.now(datetime.timezone.utc),
            'verified': False
        })
        
        return jsonify({'message': 'Game created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)})
    
@routes_blueprint.route('/api/')    
    
@routes_blueprint.route('/api/players/get/<uid>', methods=['GET'])
def get_player(uid):
    if not uid:
        return jsonify({'error': 'uid is requred to get the user'})
    
    player = db.collection('players').where("uid", "==", uid).get()
    return jsonify(player[0].to_dict())