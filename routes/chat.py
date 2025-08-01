import json
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from fuzzywuzzy import process

load_dotenv()

chat_bp = Blueprint('chat', __name__)

# Cargar el token de Hugging Face desde variable de entorno
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

MODEL_NAME = "google/gemma-2b-it"

if HF_TOKEN:
    # Si existe el token, cargar el tokenizer y el modelo
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, token=HF_TOKEN)
else:
    # Si no hay token, no cargar modelo para evitar errores en tests u otros entornos
    tokenizer = None
    model = None
    print("⚠️ WARNING: HUGGINGFACE_TOKEN no está definido. El endpoint /chat no funcionará correctamente sin el token.")

# Cargar base de conocimiento
with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)

def buscar_contexto(mensaje_usuario):
    preguntas = [item['question'] for item in knowledge_base]
    mejor_match, score = process.extractOne(mensaje_usuario, preguntas)
    if score > 60:
        for item in knowledge_base:
            if item['question'] == mejor_match:
                return item['answer']
    return ""

@chat_bp.route('/chat', methods=['POST'])
def chat():
    if not tokenizer or not model:
        return jsonify({"error": "El token de Hugging Face no está configurado. Servicio no disponible."}), 503

    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "Falta el mensaje"}), 400

    try:
        contexto = buscar_contexto(message)
        prompt = f"Información relevante: {contexto}\nUsuario: {message}\nAsistente:"
        inputs = tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=100, do_sample=True)

        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if "Asistente:" in response_text:
            response_text = response_text.split("Asistente:")[-1].strip()

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
