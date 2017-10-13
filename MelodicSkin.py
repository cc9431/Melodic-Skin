'''Testing out code for a friend's art project about turning skin tone into sound'''
# Charles Calder <cc9431@bard.edu>
# September 7th 2017

import sys
import math
import wave
from PIL import Image, ImageDraw
import pyaudio

class TonePlayer(object):
    '''Class for all aspects of the code that relate to creating,
    playing, and saving the data stream of tones created out of the images'''
    MAXFREQ = 1500.00
    BITRATE = 44100
    DURATION = 0.1
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.data = ''

    def pixel_to_tone(self, tup_array):
        '''Combine multiple functions to turn a list of colors into a list of tones'''
        for tup_pixel in tup_array:
            self.freq_to_tone(self.pixel_to_freq(tup_pixel))

    def pixel_to_freq(self, tup_pixel):
        '''Given rgb values, convert those into a frequency on the audible spectrum'''
        color = tup_pixel[1]
        val = (((65536.0*color[0]) + (256.0*color[1]) + color[2])/16777215.0)
        return val*TonePlayer.MAXFREQ

    def freq_to_tone(self, freq, amplitude=1):
        '''Add a datum (one note) to our data given a certain frequency'''
        numOfFrames = int(TonePlayer.BITRATE * TonePlayer.DURATION)
        datum = self.sin_wave(freq, amplitude, numOfFrames)
        self.data += datum

    def sin_wave(self, freq, amplitude, frame_num):
        '''Convert a frequency/amplitude/frame number into a tone for our data stream'''
        chars = ''
        for frame in xrange(frame_num):
            sin = (math.sin(frame / ((TonePlayer.BITRATE / freq) / math.pi)) * 127 + 128)
            chars += chr(int(amplitude * sin))
        return chars

    def test_scale(self):
        '''play a scale to test pyaudio'''
        scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
        for freq in scale:
            self.freq_to_tone(freq)

    def play(self):
        '''Play a stream of data'''
        self.stream = self.pa.open(
            format=self.pa.get_format_from_width(1),
            channels=1,
            rate=TonePlayer.BITRATE,
            output=True)
        self.stream.write(self.data)
        self.stream.stop_stream()
        self.stream.close()

    def save_wave(self, output_file_name):
        '''Save the current data stream to a .wav file'''
        waveFile = wave.open(output_file_name, 'wb')
        waveFile.setnchannels(1)
        waveFile.setsampwidth(self.pa.get_sample_size(self.pa.get_format_from_width(1)))
        waveFile.setframerate(TonePlayer.BITRATE)
        waveFile.writeframes(self.data)
        waveFile.close()

class Portrait(object):
    '''Class for all aspects of this program that are involved with image processing'''
    def __init__(self, file_path, save_path, array_length=50, thresh=100, col_size=20):
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
        self.min_heap_sort()
        self.remove_white()
        if resz:
            self.resize()
        if save:
            self.draw_and_save()

    def remove_white(self):
        '''removes any pixel with a color that is similair to the most common color'''
        top_color = self.tuple_array[0][1]
        #print top_color
        new_array = []
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
            draw.rectangle(x_y, count_color[1])#, (0, 0, 0))
        del draw
        self.img.save(self.save_to_file)

    def resize(self):
        '''Resize our tuple array'''
        self.tuple_array = [self.tuple_array[x] for x in xrange(self.length)]

    def swap(self, i, j):
        '''Swap two values given thier position in the array'''
        self.tuple_array[i], self.tuple_array[j] = self.tuple_array[j], self.tuple_array[i]

    def heapify(self, end, i):
        '''Given end of list and position value, place the value into the heap'''
        left = 2 * i
        right = (2 * i) + 1
        min_num = i
        if left < end and self.tuple_array[i] > self.tuple_array[left]:
            min_num = left
        if right < end and self.tuple_array[min_num] > self.tuple_array[right]:
            min_num = right
        if min_num != i:
            self.swap(i, min_num)
            self.heapify(end, min_num)

    def min_heap_sort(self):
        '''heap sort with a min-heap, to sort the pixel array with the max number at the front'''
        last = len(self.tuple_array) - 1
        first = (last // 2)
        for i in range(first, -1, -1):
            self.heapify(last, i)
        for i in range(last, -1, -1):
            self.swap(i, 0)
            self.heapify(i, 0)

def test(filepath):
    '''Function to test that the pyaudio and color analysis sides work as they should'''
    filepath_minus_extension = filepath.split(".")[0]
    savepath = filepath_minus_extension + "_result.jpg"

    tone = TonePlayer()
    port = Portrait(filepath, savepath, 150, 120)

    port.analyze(True, True)
    tone.pixel_to_tone(port.tuple_array)
    tone.save_wave(filepath_minus_extension + ".wav")

if __name__ == "__main__":
    # Take the first argument from the command line as the image file to process
    test(str(sys.argv[1]))
