'''
This code stimulate with a sinus function input
a LIF neuron and show the membran's voltage,
the input current and the spikes

@author: Lechekhab Samir
'''

from brian2 import *

A = 1.5
f = 200*Hz
tau = 0.15*ms
eqs = '''
dv/dt = (I-v)/tau : 1
I = A*sin(2*pi*f*t) : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='euler')
M = StateMonitor(G, variables=True, record=True)
spikeMon = SpikeMonitor(G)
run(5*ms)
print('Spike times: %s' %spikeMon.t[:])
plot(M.t/ms, M.v[0], label='v')
plot(M.t/ms, M.I[0], label='I')
for t in spikeMon.t:
	axvline(t/ms, ls='--', c='C1', lw=3)
xlabel('Time (ms)')
ylabel('v')
legend(loc='best');
show()