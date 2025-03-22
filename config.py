import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
STABLE_HORDE_API_KEY = os.getenv('STABLE_HORDE_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# URLs
STABLE_HORDE_API_URL = "https://stablehorde.net/api/v2/generate/async"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data Files
USER_DATA_FILE = "user_data.json"

# Constants
MAX_HISTORY_LENGTH = 10
BAD_WORDS = ['furry', 'fuck', 'bitch', 'kys', 'kill yourself', 'killyour self', 'kill your self']