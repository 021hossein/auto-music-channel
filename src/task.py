from spotdl import Song

from config import *
from src.downloader import Downloader
from telegram_helper import send_music, send_post
from logger import get_module_logger


# Get the logger for the current module or script
logger = get_module_logger(__name__)
downloader = Downloader(settings={'output': DOWNLOAD_PATH})


async def perform_task(song: Song):
    if DEBUG:
        # Just send track tile instead of song file
        display_name = await perform_debug_task(song)
        return display_name
    try:
        logger.info(f"Downloading {song.display_name}...")
        song, path = await downloader.search_and_download(song)

        logger.info(f"Sending {path}...")
        await send_music(BOT_TOKEN, CHAT_ID, path)

        return song.display_name
    except Exception as e:
        # Handle any exceptions that occur during the execution
        # Log the error or perform any necessary error handling
        print(f"An error occurred in task: {song.name},  {str(e)}")
        return None


async def perform_debug_task(song: Song):
    logger.info(f"Perform {song.display_name} task...")
    try:
        await send_post(BOT_TOKEN, CHAT_ID, song.display_name)
        return song.display_name

    except Exception as e:
        print(f"An error occurred in sending post: {str(e)}")
        return None
    return song.display_name
