'''Testing out code for a friend's art project about turning skin tone into sound'''
# Charlie Calder <cc9431@bard.edu>
# September 7th 2017

import sys
import wave
import math
from PIL import Image
import pyaudio

class TonePlayer(object):
    '''Class for converting lists of color into frequencies, playing them, and saving them as wav files'''

    def __init__(self, length=0.2, bitrate=44100, maxFreq=2093.00, minFreq=130.81):
        self.pa = pyaudio.PyAudio()
        self.bitrate = bitrate
        self.length = length
        self.maxFreq = maxFreq
        self.minFreq = minFreq
        self.data = ''

    def pixel_to_freq(self, pixel):
        '''Given rgb values, convert those into a frequency on the audible spectrum'''
        pass


    def freq_to_tone(self, freq, amplitude=1):
        '''Play a tone given a certain frequency'''
        # Frequency needs to be between 130.81 - 2093.00 # 261.63 = C4-note.
        numOfFrames = int(self.bitrate * self.length)
        data = ''

        for x in xrange(numOfFrames):
            data += self.sin_wave(freq, x, amplitude)

        self.data += data

    def play(self):
        '''Play a tone given a stream of data'''
        self.stream = self.pa.open(
            format=self.pa.get_format_from_width(1),
            channels=1,
            rate=self.bitrate,
            output=True)
        self.stream.write(self.data)
        self.stream.stop_stream()
        self.stream.close()

    def sin_wave(self, freq, frame, amplitude):
        '''Convert a frequency/frame/amplitude into a character for our data stream'''
        sin = (math.sin(frame / ((self.bitrate / freq) / math.pi)) * 127 + 128)
        return chr(int(amplitude * sin))
    
def test_audio():
    '''Function to test that the pyaudio side works as it should'''
    #scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
    scale2 = [400, 800, 500, 900, 700, 800]

    tp = TonePlayer()

    for freq in scale2:
        tp.freq_to_tone(freq)

    tp.play()

    tp.pa.terminate()


def quixort(self):
    '''Quicksort implementation on a tuple array'''
    self.sort()

def remove_white(self):
    '''Remove all pixels that have values around (255, 255, 255)'''
    pass

def find_skin_tone(filename):
    '''Given the file name of an image, open it, sort its pixels
    and return a list of the most common non-white pixels'''
    img = Image.open(filename)
    width, height = img.size
    pixels = img.getcolors(width * height)

    most_common_pixels = []

    # pixels.quixort()
    # pixels.remove_white()

    for pix in xrange(20):
        most_common_pixels[pix] = pixels[pix]

    return most_common_pixels
