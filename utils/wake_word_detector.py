#!python3
import pvporcupine
import pyaudio
import struct
import sys
from colorama import Fore
from halo import Halo

'''
This code was adapted from porcupine demos on github:
https://github.com/Picovoice/porcupine/blob/master/demo/python/porcupine_demo_mic.py
This is an implementation of wake-word detection using porcupine.
'''


class WakeWordDetector():
    def __init__(self, keyword):
        default_keywords = pvporcupine.KEYWORDS
        self.keyword = keyword if keyword in default_keywords else 'bumblebee'
        self.porcupine = None
        self.pa = None
        self.audio_stream = None
        self.spinner = Halo(spinner='simpleDots', interval=1000)

    def run(self):
        try:
            self.porcupine = pvporcupine.create(keywords=[self.keyword])
            self.pa = pyaudio.PyAudio()

            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            # add banners for wifi and mode:
            while True:
                self.spinner.start(text="Say '"+self.keyword+"' to activate.")
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from(
                    "h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    # Word detected
                    self.spinner.stop()
                    return True
        except KeyboardInterrupt:
            print(Fore.CYAN + 'Stopping...')
        finally:
            if self.porcupine is not None:
                self.porcupine.delete()
            if self.audio_stream is not None:
                self.audio_stream.close()
            if self.pa is not None:
                self.pa.terminate()

    def stop(self):
        print(Fore.CYAN + 'Stopping...')
        if self.porcupine is not None:
            self.porcupine.delete()
        if self.audio_stream is not None:
            self.audio_stream.close()
        if self.pa is not None:
            self.pa.terminate()
        sys.exit()
