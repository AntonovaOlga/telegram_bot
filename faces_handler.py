import os

from aiogram import types
import cv2
import numpy as np
from io import BytesIO

from pony.orm import db_session

from db import FacesPhoto
from files_handler import save_file


@db_session
async def faces_handler(message: types.Message):
    template_file = BytesIO()
    file_for_download = await message.photo[0].get_file()
    await file_for_download.download(template_file)
    template_file.seek(0)

    if with_faces(template_file):
        user_id = message.from_user.id
        file_id = file_for_download.file_unique_id
        msg_date = message.date
        file_extension = file_for_download['file_path'].split('.')[-1]
        save_path = os.path.join('img_with_faces', f'{file_id}.{file_extension}')
        save_file(template_file, save_path)
        FacesPhoto(photo_id=file_id, user_id=user_id, photo_path=save_path, date=msg_date)


def with_faces(file: BytesIO) -> bool:
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10)
    )
    file.seek(0)
    return bool(len(faces))
