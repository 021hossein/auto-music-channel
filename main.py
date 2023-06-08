import asyncio
import datetime
import os
import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from telegram_helper import send_music, send_post
from logger import get_module_logger


# Set up your Spotify API credentials
client_id = '5f2fb8894e464653bd0c2fbd81e957a6'
client_secret = '789ef1750b48450ab767e7b44eb6f2c7'
bot_token = '5927525345:AAFNHk_jxBQXof3UEW2I--3zG71485Dnh1E'
chat_id = '@EclecticEuphoria'
interval = 15

# Initialize the Spotify API client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define the Spotify playlist URI or URL
playlist_uri = 'https://open.spotify.com/playlist/0nixvGXVVYy23KDUD09e4y?si=88d8a7433512415a'


# Get the logger for the current module or script
logger = get_module_logger(__name__)


async def check_recently_added_tracks(playlist_uri):
    last_checked_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=interval)
    while True:
        logger.info("getting playlist items...")

        # Retrieve the current state of the playlist
        results = spotify.playlist_items(playlist_uri)

        logger.info(f"checking playlist for new items...")

        # Get the current time in UTC
        current_time = datetime.datetime.utcnow()

        # Extract the track information from the retrieved tracks
        for track in results['items']:
            track_name = track['track']['name']
            added_at = track['added_at']
            artist_name = track['track']['artists'][0]['name']
            url = track['track']['external_urls']['spotify']
            path = f"./{artist_name} - {track_name}.mp3"

            # Convert the added_at timestamp to a datetime object
            added_time = datetime.datetime.strptime(added_at, "%Y-%m-%dT%H:%M:%SZ")

            # Calculate the time difference between current_time and added_time
            time_difference = last_checked_time - added_time
            # Check if the track was added within the last 10 seconds
            if time_difference.total_seconds() <= interval:
                logger.info(f"Recently added track: {track_name}")
                await task(url, path)

        last_checked_time = current_time
        time.sleep(interval)


async def download(url, path):
    command = f"spotdl {url}"
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()
    return path


async def task(url, path):
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

    asyncio.run(check_recently_added_tracks(playlist_uri))
    # asyncio.run(pass_spotify())
