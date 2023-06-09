import asyncio
import datetime
import time

from config import *
from telegram_helper import send_music
from logger import get_module_logger
from spotify_helper import filter_recently_added_tracks

# Define the Spotify playlist URI or URL
playlist_uri = 'https://open.spotify.com/playlist/0nixvGXVVYy23KDUD09e4y?si=88d8a7433512415a'

# Get the logger for the current module or script
logger = get_module_logger(__name__)


async def check_recently_added_tracks(playlist_uri, interval):
    last_checked_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=interval)
    while True:
        logger.info("Getting playlist items...")
        try:
            new_tracks = filter_recently_added_tracks(playlist_uri, last_checked_time)
            current_time = datetime.datetime.utcnow()

            for track in new_tracks:
                logger.info(f"Recently added track: {track['track_name']}")
                asyncio.create_task(perform_task(track['url'], track['file_name']))

            last_checked_time = current_time
            await asyncio.sleep(interval)

        except Exception as e:
            # Handle any exceptions that occur during the execution
            logger.error(f"An error occurred: {str(e)}")
            # Decide how to handle the error based on your specific requirements


async def download(url, file_name):
    command = f'spotdl  --output "{path}" {url}'
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()
    return file_name


async def perform_task(url, file_name):
    try:
        logger.info(f"Downloading {file_name}...")
        await download(url, file_name)
        logger.info(f"Sending {file_name}...")
        await send_music(bot_token, chat_id, f'{path}{file_name}')
        # Remove file after sending
        logger.info(f"Removing {file_name}...")
        os.remove(f'{path}{file_name}')
        return file_name
    except Exception as e:
        # Handle any exceptions that occur during the execution
        # Log the error or perform any necessary error handling
        print(f"An error occurred in task: {str(e)}")
        return None


if __name__ == '__main__':
    # asyncio.run(check_recently_added_tracks(playlist_uri, interval))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_recently_added_tracks(playlist_uri, interval))
