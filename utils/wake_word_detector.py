#!python3
import pvporcupine
import pyaudio
import struct
import os
import sys
from colorama import Fore

'''
This code was adapted from porcupine demos on github: https://github.com/Picovoice/porcupine/blob/master/demo/python/porcupine_demo_mic.py
This is an implementation of wake-word detection using porcupine.
'''
porcupine = None
pa = None
audio_stream = None

def run():
    try:
        porcupine = pvporcupine.create(keywords=['bumblebee']) # part of default keywords from porcupine.
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length)
        print(Fore.CYAN + '[Listening...]')
        # add banners for wifi and mode:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                # Word detected
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
