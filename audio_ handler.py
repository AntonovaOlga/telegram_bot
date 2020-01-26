# -*- coding: utf-8 -*-

import subprocess


def oga_to_wav_convert(oga_file, wav_file, wav_hz=16000):
    oga_to_wav_comand = f'ffmpeg -i {oga_file} -ar {wav_hz} {wav_file}'
    subprocess.call(oga_to_wav_comand)


if __name__=='__main__':
    