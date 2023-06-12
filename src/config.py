import os
from dotenv import load_dotenv

load_dotenv()

# Get proxy configuration from environment variables
proxy_host = os.getenv('PROXY_HOST', None)
proxy_port = os.getenv('PROXY_PORT', None)

# Set up the proxy for requests library if the configuration is set
proxies = {}
if proxy_host and proxy_port:
    proxies = {
        'http': f'http://{proxy_host}:{proxy_port}',
        'https': f'http://{proxy_host}:{proxy_port}',
    }

# Set default values for other variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
playlist_uris = os.getenv('PLAYLIST_URIS', '').split(',')
interval = int(os.getenv('INTERVAL', '60'))
max_concurrent_tasks = int(os.getenv('MAX_CONCURRENT_TASKS', '5'))
tracks_limit = int(os.getenv('TRACKS_LIMIT', '50'))
download_path = './download/{artist}/{album}/{track-number} - {title}'

# logging_pending_counter_interval, set 0 for disabling
logging_interval = int(os.getenv('LOGGING_INTERVAL', '5'))

