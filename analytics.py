import json
import os

FILE_PATH = "analytics_data.json"

def load_data():
    # 🚨 HARD MILESTONE: Setting base to your latest success
    base_stats = {"visits": 386, "analyses": 46}
    
    if not os.path.exists(FILE_PATH):
        return base_stats
    
    try:
        with open(FILE_PATH, "r") as f:
            stored_data = json.load(f)
            # Agar stored data restart ki wajah se base stats se kam hai, toh base return karo
            if stored_data.get("visits", 0) < base_stats["visits"]:
                return base_stats
            return stored_data
    except:
        return base_stats

def save_data(data):
    try:
        with open(FILE_PATH, "w") as f:
            json.dump(data, f)
    except:
        pass

def track_visit():
    data = load_data()
    data["visits"] += 1
    save_data(data)

def track_analysis():
    data = load_data()
    data["analyses"] += 1
    save_data(data)