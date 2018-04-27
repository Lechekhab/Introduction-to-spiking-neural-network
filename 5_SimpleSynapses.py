'''
Simple demonstartion de l'utilisation de synapses pour
connecter 4 neurones entre eux.

@author: Lechekhab Samir
@source: https://brian2.readthedocs.io/en/2.0rc/resources/tutorials/2-intro-to-brian-synapses.html
'''

from brian2 import *
from brian2tools import *

eqs ='''
dv/dt = (I-v)/tau : 1
I : 1
tau : second
'''

G = NeuronGroup(4, eqs, threshold='v>0.9', reset='v = 0', method='exact')
G.I = [1, 0, 0, 0]
G.tau = [10, 100, 100, 100]*ms

S = Synapses(G, G, 'w : 1', on_pre='v_post += w')
S.connect(i=0, j=[1, 2, 3])
S.w = '0.2+j*0.2'

M = StateMonitor(G, 'v', record=True)
spikeMon = SpikeMonitor(G)

run(100*ms)
brian_plot(M)
show()
