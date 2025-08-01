import json
import sys
import os
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def test_register_and_login():
    client = app.test_client()

    user_data = {
        "username": "testuser",
        "password": "testpass"
    }

    response = client.post("/users/register", json=user_data)
    assert response.status_code in [200, 201, 400]  # 201 creado, 400 ya existe

    login_resp = client.post("/users/login", json=user_data)
    assert login_resp.status_code == 200
    assert "token" in json.loads(login_resp.data)

# Aquí hacemos patch directo al método chat para que devuelva una respuesta simulada.
from unittest.mock import patch

@patch("routes.chat.send_to_huggingface")  # Patch al endpoint chat en routes/chat.py
def test_protected_chat(mock_chat):
    # Configuramos el mock para que devuelva una respuesta JSON con status_code 200
    mock_chat.return_value = (json.dumps({"response": "Respuesta simulada"}), 200, {"Content-Type": "application/json"})

    client = app.test_client()

    # Registrar usuario
    client.post("/users/register", json={
        "username": "testuser",
        "password": "testpass"
    })

    # Login para obtener token
    login_resp = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert login_resp.status_code == 200
    data = json.loads(login_resp.data)
    assert "token" in data

    token = data["token"]

    # Llamar al endpoint protegido /chat usando el token y el mock del chat
    chat_resp = client.post("/chat", json={"message": "hola"}, headers={
        "Authorization": f"Bearer {token}"
    })

    assert chat_resp.status_code == 200
    assert b"Respuesta simulada" in chat_resp.data
