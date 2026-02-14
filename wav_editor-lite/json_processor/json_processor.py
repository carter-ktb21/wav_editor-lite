import json
from pathlib import Path

def process_json_folder(folder_path: str):
    results = []

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"{folder_path} is not a valid folder with ")
    
    for json_file in folder.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        results.append(data)

    return results