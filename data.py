import json
import os

DATA_FILE = "data.json"

def load_local_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_local_data(data_list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)

def add_new_phone(phone):
    data = load_local_data()
    data.append(phone)
    save_local_data(data)
