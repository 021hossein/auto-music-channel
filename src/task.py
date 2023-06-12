from spotdl import Song

from config import *
from src.downloader import Downloader
from telegram_helper import send_music
from logger import get_module_logger


# Get the logger for the current module or script
logger = get_module_logger(__name__)
downloader = Downloader(settings={'output': download_path})


async def perform_task(song: Song):
    try:
        logger.info(f"Downloading {song.display_name}...")
        song, path = await downloader.search_and_download(song)

        logger.info(f"Sending {path}...")
        await send_music(bot_token, chat_id, path)

        return song.display_name
    except Exception as e:
        # Handle any exceptions that occur during the execution
        # Log the error or perform any necessary error handling
        print(f"An error occurred in task: {str(e)}")
        return None
