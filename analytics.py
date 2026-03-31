import json
import os

FILE = "analytics.json"

def load_data():
    if not os.path.exists(FILE):
        return {"visits": 0, "analyses": 0}
    
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def track_visit():
    data = load_data()
    data["visits"] += 1
    save_data(data)

def track_analysis():
    data = load_data()
    data["analyses"] += 1
    save_data(data)