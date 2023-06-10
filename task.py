import asyncio

from config import *
from telegram_helper import send_music
from logger import get_module_logger


# Get the logger for the current module or script
logger = get_module_logger(__name__)


async def download(url, file_name):
    command = f'spotdl  --output "{path}" {url}'
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()
    return file_name


async def perform_task(track):
    try:
        file_name = track['file_name']
        url = track['url']
        file_path = f'{path}{file_name}'

        logger.info(f"Downloading {file_name}...")
        await download(url, file_name)

        logger.info(f"Sending {file_name}...")
        await send_music(bot_token, chat_id, file_path)

        logger.info(f"Removing {file_name}...")
        os.remove(f'{path}{file_name}')

        return file_name
    except Exception as e:
        # Handle any exceptions that occur during the execution
        # Log the error or perform any necessary error handling
        print(f"An error occurred in task: {str(e)}")
        return None
