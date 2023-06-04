import asyncio
from telegram import Bot
from telegram.constants import ParseMode
import telegram

async def send_post(token, chat_id, text):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

async def send_music(token, chat_id, audio_path):
    bot = Bot(token=token)
    await bot.send_audio(chat_id=chat_id, audio=open(audio_path, 'rb'), caption='caption')

async def send_message_and_music(token, chat_id, text, audio_path):
    await send_post(token, chat_id, text)
    await send_music(token, chat_id, audio_path)
