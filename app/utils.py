import json
import os

def load_json(file_path):
    """Loads JSON data from a specified file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_json(file_path, data):
    """Saves JSON data to a specified file."""
    with open(file_path, 'w') as f:
        json.dump(data, f)
