import asyncio
import datetime
import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import *
from telegram_helper import send_music, send_post
from logger import get_module_logger

# Set up Spotify client credentials manager
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager, proxies=proxies)

# Define the Spotify playlist URI or URL
playlist_uri = 'https://open.spotify.com/playlist/0nixvGXVVYy23KDUD09e4y?si=88d8a7433512415a'


# Get the logger for the current module or script
logger = get_module_logger(__name__)


async def check_recently_added_tracks(playlist_uri, interval):
    last_checked_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=interval)
    while True:
        logger.info("Getting playlist items...")
        try:
            # Retrieve the current state of the playlist
            results = spotify.playlist_items(playlist_uri)
            logger.info("Checking playlist for new items...")

            current_time = datetime.datetime.utcnow()

            filtered_items = filter(
                lambda track: datetime.datetime.strptime(track['added_at'], "%Y-%m-%dT%H:%M:%SZ") > last_checked_time,
                results['items']
            )

            for track in filtered_items:
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                url = track['track']['external_urls']['spotify']
                path = f"./{artist_name} - {track_name}.mp3"

                logger.info(f"Recently added track: {track_name}")
                asyncio.create_task(perform_task(url, path))

            last_checked_time = current_time
            await asyncio.sleep(interval)

        except Exception as e:
            # Handle any exceptions that occur during the execution
            logger.error(f"An error occurred: {str(e)}")
            # Decide how to handle the error based on your specific requirements


async def download(url, path):
    command = f"spotdl {url}"
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()
    return path


async def perform_task(url, path):
    try:
        logger.info(f"Downloading {path}...")
        await download(url, path)
        logger.info(f"Sending {path}...")
        await send_music(bot_token, chat_id, path)
        # Remove file after sending
        logger.info(f"Removing {path}...")
        os.remove(path)
        return path
    except Exception as e:
        # Handle any exceptions that occur during the execution
        # Log the error or perform any necessary error handling
        print(f"An error occurred in task: {str(e)}")
        return None


if __name__ == '__main__':

    # asyncio.run(check_recently_added_tracks(playlist_uri, interval))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_recently_added_tracks(playlist_uri, interval))
