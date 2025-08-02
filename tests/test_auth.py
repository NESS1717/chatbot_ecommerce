import json
import sys
import os
from unittest.mock import patch
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

@patch("routes.chat.send_to_huggingface")  # Patch para no llamar a Hugging Face real
def test_protected_chat(mock_chat):
    mock_chat.return_value = "Respuesta simulada"

    with app.test_client() as client:
        app.config["TESTING"] = True  # Modo testing solo dentro del contexto

        # Registro de usuario
        client.post("/users/register", json={
            "username": "testuser",
            "password": "testpass"
        })

        # Login y obtención de token
        login_resp = client.post("/users/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        assert login_resp.status_code == 200
        data = json.loads(login_resp.data)
        assert "token" in data

        token = data["token"]

        # Envío al endpoint /chat con token
        chat_resp = client.post("/chat", json={"message": "hola"}, headers={
            "Authorization": f"Bearer {token}"
        })

        assert chat_resp.status_code == 200
        assert b"Respuesta simulada" in chat_resp.data


