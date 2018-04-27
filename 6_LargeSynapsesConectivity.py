'''
This code create a neural network
with many synapses and show the 
connectivity.

@author: Lechekhab Samir
'''

from brian2 import *
import colorsys
import numpy as np

gmax = 1.0

eqs = '''
dv/dt = (I-v)/tau : 1
I : 1
tau : second
'''

G = NeuronGroup(20, eqs, threshold='v>1', reset='v = 0')

S = Synapses(G, G, 'w : 1', on_pre='v_post += w')
S.connect(p=0.8)
S.w = 'rand()*gmax'

def plot_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10,4))
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0,1], [i,j],'-', color=colorsys.hls_to_rgb(float(S.w[i,j]*(0.33/gmax)),0.5,1.0)) #3.3 for a color range form red to green
        print(S.w[i,j])
    xticks([0,1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    show()

plot_connectivity(S)