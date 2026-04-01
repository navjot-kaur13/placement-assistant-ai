import json
import os

# Server restart par data loss bachane ke liye base numbers
FILE_PATH = "analytics_data.json"

def load_data():
    # Aapka actual traction jo aaj reach hua tha
    base_stats = {"visits": 105, "analyses": 6}
    
    if not os.path.exists(FILE_PATH):
        return base_stats
    
    try:
        with open(FILE_PATH, "r") as f:
            stored_data = json.load(f)
            # Agar stored data restart ki wajah se base stats se kam dikh raha hai, 
            # toh hum base stats (105) hi dikhayenge.
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