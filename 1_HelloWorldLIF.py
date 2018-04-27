'''
Visualisation d'emission d'impulsions
avec un neurone de type LIF avec un 
courant d'entrée constant.

@author: Lechekhab Samir
'''
from brian2 import *

tau = 5*ms
v_th = 'v>0.8'
v_rst = 'v=0'
eqs = '''
dv/dt = (1-v)/tau : 1
'''

LIF = NeuronGroup(1, eqs, threshold=v_th, reset=v_rst, method='exact')
Monitor = StateMonitor(LIF, 'v', record=0)
spikeMon = SpikeMonitor(LIF)
run(25*ms)
print('Spike times: %s' %spikeMon.t[:])
plot(Monitor.t/ms, Monitor.v[0])
for t in spikeMon.t:
	axvline(t/ms, ls='--', c='C1', lw=3)
xlabel('Time (ms)')
ylabel('v')
title('Constant stimuli LIF');
show()