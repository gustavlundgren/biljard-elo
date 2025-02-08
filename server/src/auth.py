from flask import Blueprint, request, jsonify
from firebase_admin import auth

auth_blueprint = Blueprint('auth', __name__)
      
@auth_blueprint.route('/api/auth', methods=['POST'])
def login():
    data = request.json
    token = data.get('token')
    email = data.get('email')
    
    if not token:
        return jsonify({'error': 'Token is needed'}), 401
    
    if not email:
        return jsonify({'error': 'Email needed'}), 401
    
    try:
        decoded_token = auth.verify_id_token(token)
        
        if decoded_token['email'] != email:
            return jsonify({'error': 'Incorrect token for this user'}), 401
        
        return jsonify({'uid': decoded_token['uid']}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 401
