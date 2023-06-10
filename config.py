import os

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
client_id = os.getenv('CLIENT_ID', '5f2fb8894e464653bd0c2fbd81e957a6')
client_secret = os.getenv('CLIENT_SECRET', '789ef1750b48450ab767e7b44eb6f2c7')
bot_token = os.getenv('BOT_TOKEN', '5927525345:AAFNHk_jxBQXof3UEW2I--3zG71485Dnh1E')
chat_id = os.getenv('CHAT_ID', '@EclecticEuphoria')
interval = int(os.getenv('INTERVAL', '60'))
max_concurrent_tasks = int(os.getenv('MAX_CONCURRENT_TASKS', '5'))
playlist_uri = os.getenv('PLAYLIST_URI', 'https://open.spotify.com/playlist/0nixvGXVVYy23KDUD09e4y?si=88d8a7433512415a')
path = './music/'
