#!python3
import pvporcupine
import pyaudio
import struct
import os
import sys
from colorama import Fore
from halo import Halo

'''
This code was adapted from porcupine demos on github:
https://github.com/Picovoice/porcupine/blob/master/demo/python/porcupine_demo_mic.py
This is an implementation of wake-word detection using porcupine.
'''
porcupine = None
pa = None
audio_stream = None
spinner = Halo(spinner='simpleDots', interval=1000)


def run():
    try:
        # 'bumblebee is one of default keywords from porcupine.
        porcupine = pvporcupine.create(keywords=['bumblebee'])
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
            )

        # add banners for wifi and mode:
        while True:
            spinner.start(text="Say 'Bumblebee' to activate.")
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                # Word detected
                spinner.stop()
                return True
    except KeyboardInterrupt:
        print(Fore.CYAN + 'Stopping...')
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


def stop():
    print(Fore.CYAN + 'Stopping...')
    if porcupine is not None:
        porcupine.delete()
    if audio_stream is not None:
        audio_stream.close()
    if pa is not None:
        pa.terminate()
    sys.exit()
