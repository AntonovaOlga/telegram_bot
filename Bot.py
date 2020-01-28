# -*- coding: utf-8 -*-
import logging

from faces_handler import faces_handler
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from pony.orm import db_session

from voice_handler import voice_handler

try:
    from settings import API_TOKEN, PROXY_URL, PROXY_LOGIN, PROXY_PASSWORD
except Exception:
    exit("Do cp settings.py.default settings.py and set API_TOKEN and proxy info")

logging.basicConfig(level=logging.INFO)
PROXY_AUTH = aiohttp.BasicAuth(
    login=PROXY_LOGIN,
    password=PROXY_PASSWORD
)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

START_MSG = "TTestBotForDSP save all audio message and convert in WAVE format, and save photo with faces "


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(START_MSG)


@dp.message_handler(content_types=types.ContentType.VOICE)
async def voice_message_handler(message: types.Message):
    logging.info('Поступило голосовое сообщение')
    await voice_handler(message)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_massage_handler(message: types.Message):
    logging.info('Поступила картинка')
    await faces_handler(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
