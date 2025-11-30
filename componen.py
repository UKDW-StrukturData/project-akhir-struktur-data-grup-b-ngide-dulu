import json
import os

def load_users():
    """Memuat database user dari file JSON"""
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"admin": "password123"}
    return {"admin": "password123"}

def save_users(data):
    """Menyimpan database user ke file JSON"""
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)