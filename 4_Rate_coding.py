'''
This code show how to encode a analog
value in frequency of spiking

@author: Lechekhab Samir
'''

from brian2 import *

linearInput=[1,2,3,4,5,6,7,8,9,10]
ta = TimedArray(linearInput, dt=5*ms)

tau = 5*ms
v_th = 'v>0.8'
v_rst = 'v=0'
eqs = '''
dv/dt = (I-v)/tau : 1
I = ta(t) : 1
'''

LIF = NeuronGroup(1, eqs, threshold=v_th, reset=v_rst, method='exact')
Monitor = StateMonitor(LIF, variables=True, record=0)
spikeMon = SpikeMonitor(LIF)
run(50*ms)
print('Spike times: %s' %spikeMon.t[:])
plot(Monitor.t/ms, Monitor.v[0])
plot(Monitor.t/ms, Monitor.I[0], label='I1')
for t in spikeMon.t:
	axvline(t/ms, ls='--', c='C8', lw=3)
xlabel('Time (ms)')
ylabel('v')
title('Rate coding');
show()