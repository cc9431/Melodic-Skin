'''Testing out code for a friend's art project about turning skin tone into sound'''
# Charlie Calder <cc9431@bard.edu>
# September 7th 2017

import colorsys
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
        return colorsys.rgb_to_hsv(pixel[1][0], pixel[1][1], pixel[1][2])


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

    def test_scale(self):
        '''play a scale to test pyaudio'''
        scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
        for freq in scale:
            self.freq_to_tone(freq)

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

class Portrait(object):
    '''Class for converting images into usable tuple arrays of (count, color)'''

    def __init__(self, file_path, save_path, array_length=50, thresh=110, col_size=20):
        self.path_to_file = file_path
        self.save_to_file = save_path
        self.threshold = thresh
        self.img = Image.open(self.path_to_file)
        self.height, self.width = self.img.size
        self.tuple_array = self.img.getcolors(self.height * self.width)
        self.color_size = col_size
        self.length = array_length

    def analyze(self, resz=False, save=False):
        '''Sorts pixels and return a list of the most common non-white pixels'''
        self.heap_sort()
        self.remove_white()
        if resz:
            self.resize()
        if save:
            self.draw_and_save()

    def remove_white(self):
        '''removes any pixel with a color that is similair to the most common color'''
        top_pixel = self.tuple_array[-1]
        top_color = top_pixel[1]
        # jazz_color = (190, 140, 110)
        new_array = [(0, 0)]
        for (cnt, clr) in self.tuple_array:
            add_item = False
            for i in xrange(3):
                add_item = add_item or (abs(top_color[i] - clr[i]) > self.threshold)
            if add_item:
                new_array.append((cnt, clr))
        self.tuple_array = new_array

    def draw_and_save(self):
        '''(Meant for testing) Draws the most commonly found colors in an image onto an image'''
        draw = ImageDraw.Draw(self.img)
        length = self.height/self.color_size
        if  len(self.tuple_array) < length:
            length = len(self.tuple_array)
        for item in xrange(length):
            count_color = self.tuple_array[item]
            x_y = [0, item * self.color_size, 300, item * self.color_size + self.color_size]
            draw.rectangle(x_y, count_color[1], (0, 0, 0))
        del draw
        self.img.save(self.save_to_file)

    def resize(self):
        '''Resize our tuple array'''
        self.tuple_array = [self.tuple_array[-x-1] for x in xrange(self.length)]

    def swap(self, i, j):
        self.tuple_array[i], self.tuple_array[j] = self.tuple_array[j], self.tuple_array[i]

    def heapify(self, end, i):
        l = 2 * i + 1
        r = 2 * (i + 1)
        max_num = i
        if l < end and self.tuple_array[i] < self.tuple_array[l]:
            max_num = l
        if r < end and self.tuple_array[max_num] < self.tuple_array[r]:
            max_num = r
        if max_num != i:
            self.swap(i, max_num)
            self.heapify(end, max_num)

    def heap_sort(self):
        last = len(self.tuple_array)
        first = last // 2 - 1
        for i in range(first, -1, -1):
            self.heapify(last, i)
        for i in range(last-1, 0, -1):
            self.swap(i, 0)
            self.heapify(i, 0)

def test(filepath, savepath):
    '''Function to test that the pyaudio and color analysis sides work as they should'''
    tone = TonePlayer()

    port = Portrait(filepath, savepath)
    port.analyze(True, True)

    for cnt_col in port.tuple_array:
        print cnt_col, tone.pixel_to_freq(cnt_col)


test("TestFiles/test_obama.jpg", "TestFiles/test_obama_result.jpg")
