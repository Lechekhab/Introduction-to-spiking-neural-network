'''
This code is used to draw the spectrograms

@author: Lechekhab Samir
'''

import scipy
import matplotlib.pyplot as plt
import scipy.io.wavfile

fileName = 'Guitar/C-major_short.wav'
sample_rate, X = scipy.io.wavfile.read(fileName)
plt.specgram(X[:,0], Fs=sample_rate, xextent=(0,30))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()