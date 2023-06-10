# Telegram-Spotify Sync Bot
This is a Telegram bot that automatically syncs a Telegram channel with a Spotify playlist. It continuously monitors the Spotify playlist for new songs and sends them to the Telegram channel in real-time.

## Features
- Automatically syncs a Spotify playlist with a Telegram channel.
- Sends new songs added to the Spotify playlist to the Telegram channel.
- Customizable sync interval to control how frequently the playlist is checked.
- Limits the number of concurrent tasks to prevent overwhelming the system.
- Dockerized for easy deployment and scalability.

## Prerequisites
- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Spotify Developer Account: [Create an App](https://developer.spotify.com/dashboard/applications)
- Telegram Bot Token: [Create a Bot](https://core.telegram.org/bots#botfather)

## Configuration
Before running the bot, you need to set the following environment variables:

- `CLIENT_ID`: Spotify client ID from your Spotify developer account.
- `CLIENT_SECRET`: Spotify client secret from your Spotify developer account.
- `BOT_TOKEN`: Telegram bot token obtained from the BotFather.
- `CHAT_ID`: Telegram channel ID where you want to send the synced songs.
- `PLAYLIST_URI`: Spotify playlist URI that you want to sync.
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
3. Set Up Configuration
Create a `.env` file in the root directory of the project and populate it with the following environment variables:

```
CLIENT_ID=<your-spotify-client-id>
CLIENT_SECRET=<your-spotify-client-secret>
BOT_TOKEN=<your-telegram-bot-token>
CHAT_ID=<your-telegram-channel-id>
PLAYLIST_URI=<your-spotify-playlist-uri>
INTERVAL=<interval-in-seconds>
MAX_CONCURRENT_TASKS=<max-concurrent-tasks>
```

Make sure to replace `<your-spotify-client-id>`, `<your-spotify-client-secret>`, `<your-telegram-bot-token>`, `<your-telegram-channel-id>`, `<your-spotify-playlist-uri>`, `<interval-in-seconds>`, and `<max-concurrent-tasks>` with your actual values.

4. Run the Bot
You can run the bot using the following command:
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
  -e CLIENT_ID=<your-spotify-client-id> \
  -e CLIENT_SECRET=<your-spotify-client-secret> \
  -e BOT_TOKEN=<your-telegram-bot-token> \
  -e CHAT_ID=<your-telegram-channel-id> \
  -e PLAYLIST_URI=<your-spotify-playlist-uri> \
  -e INTERVAL=<interval-in-seconds> \
  -e MAX_CONCURRENT_TASKS=<max-concurrent-tasks> \
  telegram-spotify-sync-bot
```
Make sure to replace `<your-spotify-client-id>`, `<your-spotify-client-secret>`, `<your-telegram-bot-token>`, `<your-telegram-channel-id>`, `<your-spotify-playlist-uri>`, `<interval-in-seconds>`, and `<max-concurrent-tasks>` with your actual values.

The bot will start running inside the Docker container, syncing the Telegram channel with the Spotify playlist.

That's it! You have set up and configured the Telegram-Spotify Sync Bot. Enjoy automatic synchronization of your Spotify playlist with your Telegram channel!

### License
This project is licensed under the MIT License. See the LICENSE file for details.


