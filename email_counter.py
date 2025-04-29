import json
import os
from datetime import datetime

COUNTER_FILE = 'email_counter.json'

PROGRESSION_PLAN = [1, 2, 3, 5, 8, 10, 15, 20]

def initialize_counter():
    if not os.path.exists(COUNTER_FILE):
        counter = {
            "progression_index": 0,
            "history": {}
        }
        save_counter(counter)

def load_counter():
    initialize_counter()
    with open(COUNTER_FILE, 'r') as f:
        return json.load(f)

def save_counter(counter_data):
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counter_data, f, indent=4)

def increment_today_count():
    today_str = datetime.now().strftime("%Y-%m-%d")
    counter = load_counter()

    # If first email of the day, move progression index forward
    if today_str not in counter['history']:
        counter['progression_index'] = min(counter['progression_index'] + 1, len(PROGRESSION_PLAN) - 1)
        counter['history'][today_str] = {"emails_sent": 0}

    counter['history'][today_str]['emails_sent'] += 1
    save_counter(counter)
    return counter['history'][today_str]['emails_sent']

def get_today_count():
    today_str = datetime.now().strftime("%Y-%m-%d")
    counter = load_counter()
    return counter['history'].get(today_str, {}).get('emails_sent', 0)

def get_daily_max_limit():
    counter = load_counter()
    progression_index = counter.get('progression_index', 0)
    return PROGRESSION_PLAN[progression_index]
