'''Testing out code for a friend's art project about turning skin tone into sound'''
# Charlie Calder <cc9431@bard.edu>
# September 7th 2017

import sys
import math
from PIL import Image, ImageDraw
import pyaudio

class TonePlayer(object):
    '''Class for converting lists of color into frequencies,
    playing them, and saving them as wav files'''

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

    def sin_wave(self, freq, frame, amplitude):
        '''Convert a frequency/frame/amplitude into a character for our data stream'''
        sin = (math.sin(frame / ((self.bitrate / freq) / math.pi)) * 127 + 128)
        return chr(int(amplitude * sin))

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

def test_audio():
    '''Function to test that the pyaudio side works as it should'''
    #scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
    scale2 = [400, 800, 500, 900, 700, 800]

    tp = TonePlayer()

    for freq in scale2:
        tp.freq_to_tone(freq)

    tp.play()

    tp.pa.terminate()



def swap(tuple_array, i, j):
    tuple_array[i], tuple_array[j] = tuple_array[j], tuple_array[i]

def heapify(tuple_array, end, i):
    l = 2 * i + 1
    r = 2 * (i + 1)
    max_num = i
    if l < end and tuple_array[i] < tuple_array[l]:
        max_num = l
    if r < end and tuple_array[max_num] < tuple_array[r]:
        max_num = r
    if max_num != i:
        swap(tuple_array, i, max_num)
        heapify(tuple_array, end, max_num)

def heap_sort(tuple_array):
    last = len(tuple_array)
    first = last // 2 - 1
    for i in range(first, -1, -1):
        heapify(tuple_array, last, i)
    for i in range(last-1, 0, -1):
        swap(tuple_array, i, 0)
        heapify(tuple_array, i, 0)

def remove_white(self):
    '''Remove all pixels that have values around (255, 255, 255)'''
    pass

def find_common_colors(filename):
    '''Given the file name of an image, open it, sort its pixels
    and return a list of the most common non-white pixels'''
    img = Image.open(filename)
    width, height = img.size
    pixels = img.getcolors(width * height)

    most_common_pixels = []

    heap_sort(pixels)
    # remove_white(pixels)

    for pix in xrange(30):
        col_count = pixels[-pix-1]
        col = col_count[1]
        if col[0] < 250 and col[1] < 250 and col[2] < 250:
            most_common_pixels.append(pixels[-pix-1])

    return most_common_pixels

def test_pixel_count():
    '''Test function to make sure pixel counting works'''
    awesomelist = find_common_colors("test_no_bkgn.jpg")

    im = Image.open("test_no_bkgn.jpg")

    draw = ImageDraw.Draw(im)
    for item in xrange(len(awesomelist)):
        color_count = awesomelist[item]
        draw.rectangle([0, item * 20, 300, (item * 20) + 20], color_count[1], (0, 0, 0))
    del draw

    im.save("test_no_bkgn_result.jpg")
