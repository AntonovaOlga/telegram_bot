import logging
import os
from pprint import pprint
import requests
import re

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

API_TOKEN = '907319109:AAFQEUR38BHEI4bNRKo7LkIBrb1Vi4nUcTs'

PROXY_URL = "socks5://ragnarok.imagespark.ru:1080"
PROXY_AUTH = aiohttp.BasicAuth(
    login='tg',
    password='E32mHfxiuuV4Mb7rE2IbvAZETMc'
)
START_MSG = "TestBotForDSP save all audio message in WAVE format and picture with faces "

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)


async def save_file(message: types.Message, msg_type: str):
    user_id = message.from_user.id
    file_id = message[msg_type].file_unique_id
    file_for_download = await message.voice.get_file()
    save_path_dir = os.path.join('voice_files', f'{user_id}')
    if not os.path.exists(save_path_dir):
        os.makedirs(save_path_dir)
    file_extension = file_for_download['file_path'].split('.')[-1]
    save_path = os.path.join(f'{save_path_dir}', f'{file_id}.{file_extension}')
    await file_for_download.download(save_path)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(START_MSG)


@dp.message_handler(content_types=ContentType.VOICE)
async def voice_handler(message: types.Message):
    logging.info('Поступило голосовое сообщение')
    await save_file(message, 'voice')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
