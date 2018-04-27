'''
This code stimulate with a wave audio signal
a LIF neuron and show the membran's voltage,
the input current and the spikes

@author: Lechekhab Samir
'''

from brian2 import *
import numpy as np
import wave
import sys
from scipy.io.wavfile import read

signal = numpy.array(read("ksp.wav")[1],dtype=float)
ta = TimedArray(signal/500, dt=0.1*ms) 
 #plot(signal/500)

tau = 5*ms
eqs = '''
dv/dt = (I-v)/tau : 1
I = ta(t, i) : 1
'''
G1 = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='euler')
M1 = StateMonitor(G1, variables=True, record=True)
spikeMon1 = SpikeMonitor(G1)
run(700*ms)
plot(M1.t/ms, M1.v[0], label='v1')
plot(M1.t/ms, M1.I[0], label='I1')
for t in spikeMon1.t:
	axvline(t/ms, ls='--', c='C8', lw=3)
xlabel('Time (ms)')
ylabel('v')
legend(loc='best');
show()