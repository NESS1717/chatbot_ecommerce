from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta

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

    stored_password = USERS_DB.get(username)

    if stored_password != password:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    access_token = create_access_token(
        identity=username,
        expires_delta=timedelta(hours=1)
    )

    return jsonify({'access_token': access_token}), 200



