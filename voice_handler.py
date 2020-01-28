# -*- coding: utf-8 -*-
import os
import subprocess
from aiogram import types
from io import BytesIO

from pony.orm import db_session

from db import VoiceMSG
from files_handler import save_file


@db_session
async def voice_handler(message: types.Message):
    template_file = BytesIO()
    file_for_download = await message.voice.get_file()
    await file_for_download.download(template_file)
    template_file.seek(0)

    user_id = message.from_user.id
    file_id = message.voice.file_unique_id
    msg_date = message.date
    file_extension = file_for_download['file_path'].split('.')[-1]
    save_path = os.path.join('voice_files', f'{user_id}', f'{file_id}.{file_extension}')
    save_file(template_file, save_path)

    wav_path = os.path.join('voice_wav_files', f'{user_id}', f'{file_id}.wav')
    oga_to_wav_convert(save_path, wav_path)
    VoiceMSG(voice_id=file_id, user_id=user_id, oga_path=save_path, wav_path=wav_path, date=msg_date)


def oga_to_wav_convert(oga_file: str, wav_file: str, wav_hz=16000):
    wav_file_dir = os.path.dirname(wav_file)
    if not os.path.exists(wav_file_dir):
        os.makedirs(wav_file_dir)
    oga_to_wav_comand = f'ffmpeg -i {oga_file} -ar {wav_hz} {wav_file}'
    subprocess.call(oga_to_wav_comand, shell=True)
