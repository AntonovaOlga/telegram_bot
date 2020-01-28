import os
from io import BytesIO


def save_file(file: BytesIO, save_path: str):
    save_path_dir = os.path.dirname(save_path)
    if not os.path.exists(save_path_dir):
        os.makedirs(save_path_dir)
    with open(save_path, 'wb') as output_file:
        output_file.write(file.read())
