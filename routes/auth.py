
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Faltan credenciales"}), 400

    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if not user:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
