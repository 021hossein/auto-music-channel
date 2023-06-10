# Telegram-Spotify Sync Bot
This is a Telegram bot that automatically syncs a Telegram channel with one or more Spotify playlists. It continuously monitors the Spotify playlist for new songs and sends them to the Telegram channel in real-time.

## Features
- **Real-time Sync**: The bot continuously monitors the specified Spotify playlists for new songs and sends them to the corresponding Telegram channels in real-time.
- **Multi-Playlist Support**: The bot supports syncing multiple Spotify playlists with their respective Telegram channels.
- **Customizable Interval**: You can configure the interval at which the bot checks for new songs in the playlists.
- **Concurrent Processing**: The bot can process multiple songs concurrently, allowing for faster synchronization.

## Prerequisites
- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Spotify Developer Account: [Create an App](https://developer.spotify.com/dashboard/applications)
- Telegram Bot Token: [Create a Bot](https://core.telegram.org/bots#botfather)

## Configuration
Before running the bot, you need to set the following environment variables:

- `CLIENT_ID`: Spotify client ID from your Spotify developer account.
- `CLIENT_SECRET`: Spotify client secret from your Spotify developer account.
- `BOT_TOKEN`: Telegram bot token obtained from the BotFather.
- `CHAT_ID`: Telegram channel ID where you want to send the songs.
- `PLAYLIST_URIS`: Comma-separated list of Spotify playlist URIs
- `TRACKS_LIMIT`: (optional) The maximum number of tracks to retrieve from each playlist in each check interval. default is 50 tracks.
- `INTERVAL`: (optional) Sync interval in seconds. Default is 60 seconds.
- `MAX_CONCURRENT_TASKS`: (optional) Maximum number of concurrent tasks. Default is 5.


## Usage
To set up and run the Telegram-Spotify Sync Bot in your local machine, follow the steps below:

1. Clone the Repository:

```
git clone https://github.com/021hossein/telegram-spotify-sync-bot.git
cd telegram-spotify-sync-bot
```
2. Install Dependencies:

```
pip install -r requirements.txt
```
3. Set Up Configuration:

Create a `.env` file in the root directory of the project and populate it with the following environment variables:

```
CLIENT_ID=your-spotify-client-id
CLIENT_SECRET=your-spotify-client-secret
BOT_TOKEN=your-telegram-bot-token
CHAT_ID=your-telegram-channel-id
PLAYLIST_URIS=spotify-playlist-uri1,spotify-playlist-uri2
TRACKS_LIMIT=100
INTERVAL=60
MAX_CONCURRENT_TASKS=5
```

Make sure to replace `<your-spotify-client-id>`, `<your-spotify-client-secret>`, `<your-telegram-bot-token>`, `<your-telegram-channel-id>`, `<your-spotify-playlist-uris>`, `<interval-in-seconds>`, and `<max-concurrent-tasks>` with your actual values.

4. Run the Bot
```
python src/main.py
```
The bot will start syncing the Telegram channel with the Spotify playlist and automatically send new songs as they are added.

## Docker
Alternatively, you can run the bot in a Docker container. To do so, follow the steps below:

1. Build the Docker Image:
```
docker build -t telegram-spotify-sync-bot .
```

2. Run the Docker Container:
```
docker run -d --name telegram-spotify-sync-bot \
  -e CLIENT_ID=your-spotify-client-id \
  -e CLIENT_SECRET=your-spotify-client-secret \
  -e BOT_TOKEN=your-telegram-bot-token \
  -e CHAT_ID=your-telegram-channel-id \
  -e PLAYLIST_URIS=spotify-playlist-uri1,spotify-playlist-uri2 \
  -e TRACKS_LIMIT=100 \
  -e INTERVAL=60 \
  -e MAX_CONCURRENT_TASKS=5 \
  telegram-spotify-sync-bot
```

The bot will start running inside the Docker container, syncing the Telegram channel with the Spotify playlist.

That's it! You have set up and configured the Telegram-Spotify Sync Bot. Enjoy automatic synchronization of your Spotify playlist with your Telegram channel!

### License
This project is licensed under the MIT License. See the LICENSE file for details.


