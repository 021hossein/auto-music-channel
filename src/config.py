import os
from dotenv import load_dotenv

load_dotenv()

# Get proxy configuration from environment variables
PROXY_HOST = os.getenv('PROXY_HOST', None)
PROXY_PORT = os.getenv('PROXY_PORT', None)

# Set up the proxy just for the spotify requests if the configuration is set
PROXIES = {}
if PROXY_HOST and PROXY_PORT:
    PROXIES = {
        'http': f'http://{PROXY_HOST}:{PROXY_PORT}',
        'https': f'http://{PROXY_HOST}:{PROXY_PORT}',
    }

# Set default values for other variables
CLIENT_ID = os.getenv('CLIENT_ID')
DEBUG = bool(int(os.getenv('DEBUG', '0')))
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
PLAYLIST_URIS = os.getenv('PLAYLIST_URIS', '').split(',')
INTERVAL = int(os.getenv('INTERVAL', '60'))
MAX_CONCURRENT_TASKS = int(os.getenv('MAX_CONCURRENT_TASKS', '5'))
TRACKS_LIMIT = int(os.getenv('TRACKS_LIMIT', '50'))
DOWNLOAD_PATH = './download/{artist}/{album}/{track-number} - {title}'

# LOGGING_INTERVAL, set 0 for disabling
LOGGING_INTERVAL = int(os.getenv('LOGGING_INTERVAL', '5'))


