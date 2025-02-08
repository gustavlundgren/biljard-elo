from flask import Blueprint, jsonify, request
from server.src import db
from firebase_admin import auth
import datetime
from server.src.elo import process_match

routes_blueprint = Blueprint('routes', __name__)

# Game routes
# GET
@routes_blueprint.route('/api/games/get', methods=['GET'])
def get_games():
    """
    Get all the games from the database
    
    Returns the data as a list of json
    """
    try:
        docs = db.collection('games').get()
        return jsonify({'data': [doc.to_dict() for doc in docs]}), 200
    except Exception as e:
        return jsonify({'error': str(e)})
    
@routes_blueprint.route('/api/games/player/<uid>', methods=['GET'])
def get_player_games(uid):
    """
    Get all the games that macth the given uid 
    """
    try:
        docs = db.collection('games').where('uid', '==', uid).get()
        return jsonify({'data': [doc.to_dict() for doc in docs]}), 200
    except Exception as e:
        return jsonify({'error': str(e)})

@routes_blueprint.route('/api/games/unverified/<uid>')
def get_unverfied_games(uid):
    """
    Get all the unverified games for a player uid
    """
    try:
        docs = db.collection('players').where('uid', '==', uid).where('verified', '==', False).get()
        return jsonify({'data': [doc.to_dict() for doc in docs]}), 200
    except Exception as e:
        return jsonify({'error': str(e)})
# POST

@routes_blueprint.route('/api/games/verify', methods=['POST'])
def verify_game():
    """
    Verify a game
    """
    data = request.json
    gid = data.get('gid')
    token = data.get('token')
    uid = ""
    
    if not gid:
        return jsonify({'error': 'Game id is needed' }), 401
    
    if not token:
        return jsonify({'error': 'Token is needed' }), 401
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

    except Exception as e:
        return jsonify({'error': str(e)})
    
    try:
        player_ref = db.collection('players').where("uid", "==", uid)
        player = player_ref.get()
        
        username = player[0].to_dict()['username']

    except Exception as e:
        return jsonify({'error': str(e)})
    
    
    try:
        game_ref = db.collection('games').document(gid)
        game = game_ref.get()
        
        if game.get('players')[1] != username:
            return jsonify({'error': 'Invalid user for verification'}), 403
        
        game_ref.update({"verified": True})
        
        return jsonify({'message': "Successfully verified the game" }), 200
    except Exception as e:
        return jsonify({'error': str(e)})
        
@routes_blueprint.route('/api/games/add', methods=['POST'])
def add_game():
    """
    Add a new game to the datatbase
    """
    data = request.json
    players = data.get('players')
    winner = data.get('winner')
    token = data.get('token')
    
    if len(players) != 2 or not winner:
        return jsonify({'error': 'Players and winner required'}), 400
    
    if winner not in players:
        return jsonify({'error': 'Winner must be one of the players in the game'}), 400
    
    if not token:
        return jsonify({'error': 'Please supply a token'}), 400
    
    try:
        players_ref = db.collection('players')
        docs = players_ref.stream()
        
        db_players = [dp.to_dict() for dp in list(docs)]
        db_usernames = [dp['username'] for dp in db_players] 
        
        if players[0] not in db_usernames or players[1] not in db_usernames:
            return jsonify({'error': 'Invalid players'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)})

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

# Players
#GET  
@routes_blueprint.route('/api/players/get/<uid>', methods=['GET'])
def get_player(uid):
    """
    Get a player with a given uid
    """
    if not uid:
        return jsonify({'error': 'uid is requred to get the user'}), 400
    
    player = db.collection('players').where("uid", "==", uid).get()
    
    if not player:
        return jsonify({'error': 'The user does not exist'}), 404
    
    return jsonify(player[0].to_dict()), 200

# POST
@routes_blueprint.route('/api/players/new', methods=['POST'])
def new_player():
    """
    Create a new player with a username and a reference to the uid of a valid user
    """
    data = request.json
    username = data.get('username')
    token = data.get("token")
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        if len(db.collection('players').where("uid", "==", uid).get()) > 0:
            return jsonify({'error': 'The user allready have a registered player'}), 403
        
        if len(db.collection('players').where('username', '==', username)):
            return jsonify({'error': 'The supplied username is taken'}), 403

        # Add a new player connected to a user with uid
        db.collection('players').add({
            "username": username,
            "elo": 1000, 
            "uid": uid
        })
        
        return jsonify({'message': 'Successfully created a player for ' + uid}), 201
        
        
    except Exception as e:
        return jsonify({'error': str(e)})