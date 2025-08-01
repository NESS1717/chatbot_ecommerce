from flask import Blueprint

root_bp = Blueprint("root", __name__)

@root_bp.route("/", methods=["GET"])
def home():
    return {"message": "Chatbot de e-commerce de ropa deportiva activo."}
