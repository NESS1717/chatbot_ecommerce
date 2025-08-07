from flask import Flask
from routes.users import users_bp
from routes.chat import chat_bp
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager  # Importa JWTManager
from pathlib import Path

###load_dotenv()
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)
print("📢 TOKEN HUGGINGFACE:", os.getenv("HUGGINGFACEHUB_API_TOKEN"))
###hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
###print("TOKEN HUGGINGFACE:", os.getenv("HUGGINGFACEHUB_API_TOKEN"))

app = Flask(__name__)
CORS(app)

# Configuraciones para JWT.
##app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_por_defecto')
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'clave_jwt_por_defecto')  # Clave para JWT
##app.config["JWT_TOKEN_LOCATION"] = ["headers"]  # De dónde se toman los tokens
print("CLAVE JWT CARGADA:", os.getenv("JWT_SECRET_KEY"))


jwt = JWTManager(app)  # Inicializa JWT con la app

app.register_blueprint(users_bp)
app.register_blueprint(chat_bp)

##if __name__ == '__main__': ###para local
  ##app.run(debug=True)   ###para local

if __name__ == "__main__":
  import os
  port = int(os.environ.get("PORT", 80))  # Puerto necesario para Azure
  app.run(host="0.0.0.0", port=port)