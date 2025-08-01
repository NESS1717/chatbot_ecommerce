from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

from utils.context import buscar_contexto
from utils.huggingface import send_to_huggingface

chat_bp = Blueprint('chat', __name__)

# Carga del modelo si existe el token
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

tokenizer = None
model = None

if hf_token:
    tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct", token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        "tiiuae/falcon-7b-instruct",
        token=hf_token,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map="auto"
    )

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "Falta el mensaje"}), 400

    try:
        contexto = buscar_contexto(message)
        prompt = f"Información relevante: {contexto}\nUsuario: {message}\nAsistente:"

        # Si estamos en testing y no hay modelo cargado, devolvemos una respuesta simulada
        if (not tokenizer or not model) and current_app.config.get("TESTING", False):
            return jsonify({"response": "Respuesta simulada"}), 200

        if not tokenizer or not model:
            return jsonify({"error": "El token de Hugging Face no está configurado. Servicio no disponible."}), 503

        response_text = send_to_huggingface(prompt)

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



