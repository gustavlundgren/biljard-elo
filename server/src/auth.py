from flask import Blueprint, request, jsonify
from firebase_admin import auth

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/api/auth', methods=['POST'])
def login():
    data = request.json
    token = data.get('token')
    
    try:
        decoded_token = auth.verify_id_token(token)
        return jsonify({'uid': decoded_token['uid']}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 401
