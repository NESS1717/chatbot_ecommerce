from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime

users_bp = Blueprint('users', __name__)

USERS_DB = {}

@users_bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Se requiere nombre de usuario y contraseña'}), 400

    if username in USERS_DB:
        return jsonify({'error': 'El usuario ya existe'}), 409

    USERS_DB[username] = password
    return jsonify({'message': 'Usuario registrado correctamente'}), 201


@users_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(f"Login attempt: username={username}, password={password}")

    stored_password = USERS_DB.get(username)
    print(f"Stored password for user: {stored_password}")

    if stored_password != password:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    SECRET_KEY = current_app.config['SECRET_KEY']

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    if isinstance(token, bytes):
        token = token.decode('utf-8')

    print(f"Generated token: {token}")

    return jsonify({'token': token})


