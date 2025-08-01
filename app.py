from flask import Flask
from routes.users import users_bp
from routes.chat import chat_bp  # <--- Agregado
from dotenv import load_dotenv
import os
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_por_defecto')

app.register_blueprint(users_bp)
app.register_blueprint(chat_bp)  # <--- Agregado

if __name__ == '__main__':
    app.run(debug=True)

