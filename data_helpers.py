import json
from config import USER_DATA_FILE

def load_user_data():
    """Load user data from file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(user_data):
    """Save user data to file."""
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4)