import os
import json
def load_users():
    filename = 'users.json'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)  # Write an empty JSON object
        return {}  # Return an empty dictionary
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save user data to a JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
def initialize_cooldowns(user_id):
    return {
        user_id: "12456789",
        'mission_cooldown': 24 * 3600,  # 24 hours in seconds
        'reminder_cooldown': 12 * 3600  # 12 hours in seconds
    }
