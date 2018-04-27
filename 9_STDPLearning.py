'''
Created on 07.04.2018

@author: Lechekhab Samir
'''


from brian2 import *
from brian2tools import *
import pickle
import os.path
import colorsys
import numpy as np
import wave
import sys
from scipy.io.wavfile import read


def simulate_weight(durationMs):
    fileObject = open(fileName,'wb') 

    run(durationMs*second, report='text')

    synapsesWeightList = []
    for i, j in zip(SHL.i, SHL.j):
        synapsesWeightList.append(SHL.w[i,j])
    pickle.dump(synapsesWeightList,fileObject)
    fileObject.close()

def load_weight():
    fileObject = open(fileName,'rb')
    synapsesWeightList = pickle.load(fileObject)
    for i, j in zip(SHL.i, SHL.j):
        SHL.w[i,j] = synapsesWeightList[i] 
    fileObject.close()

def plot_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10,4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0,1], [i,j],'-', color=colorsys.hls_to_rgb(float(S.w[i,j]*(0.33/gmax)),0.5,1.0)) #3.3 for a color range form red to green
        print(S.w[i,j])
    xticks([0,1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok', color=colorsys.hls_to_rgb(float(S.w*(0.33/gmax)),0.5,1.0))
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')

N = 100
taum = 10*ms
taupre = 20*ms
taupost = taupre
Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms
F = 15*Hz
gmax = .01
dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax
#File to save the weight of every synapses in the hidden layer
fileName = 'synapsesWeight.pkl'
#Audio signal
signal_D = numpy.array(read("Guitar/D-major_short.wav")[1],dtype=float)
ta_D = TimedArray(signal_D/50, dt=0.01*ms)

signal_C = numpy.array(read("Guitar/C-major_short.wav")[1],dtype=float)
ta_C = TimedArray(signal_C/50, dt=0.01*ms)

signal_G = numpy.array(read("Guitar/G-major_short.wav")[1],dtype=float)
ta_G = TimedArray(signal_G/50, dt=0.01*ms) 
tauInput = 10*ms
#Equation for the anolog to spike neurons converter
eqs_InputNeurons_1 = '''
dv/dt = (I-v)/taum : 1
I = ta_D(t, i) : 1
'''

eqs_InputNeurons_2 = '''
dv/dt = (I-v)/taum : 1
I = ta_C(t, i) : 1
'''

eqs_InputNeurons_3 = '''
dv/dt = (I-v)/taum : 1
I = ta_G(t, i) : 1
'''
#I = 2.5*sin(2*pi*(1000*Hz)*t) : 1

#Equation for the Hidden layer's neurons
eqs_HiddenNeurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

InputNeuron_1 = NeuronGroup(1, eqs_InputNeurons_1, threshold='v>-.054', reset='v=-.06', method='euler')
InputNeuron_2 = NeuronGroup(1, eqs_InputNeurons_2, threshold='v>-.054', reset='v=-.06', method='euler')
InputNeuron_3 = NeuronGroup(1, eqs_InputNeurons_3, threshold='v>-.054', reset='v=-.06', method='euler')

HiddenNeurons_1 = NeuronGroup(N, eqs_HiddenNeurons, threshold='v>vt', reset='v = vr',
                      method='linear')
HiddenNeurons_2 = NeuronGroup(N, eqs_HiddenNeurons, threshold='v>vt', reset='v = vr',
                      method='linear')


#Synapses Input Layer
SIL_1 = Synapses(InputNeuron_1, HiddenNeurons_1,'w : 1')
SIL_1.connect(j='k for k in range(0, 33) if i!=k', skip_if_invalid=True)
SIL_1.w = 10

SIL_2 = Synapses(InputNeuron_2, HiddenNeurons_1,'w : 1')
SIL_2.connect(j='k for k in range(34, 66) if i!=k', skip_if_invalid=True)
SIL_2.w = 10

SIL_3 = Synapses(InputNeuron_3, HiddenNeurons_1,'w : 1')
SIL_3.connect(j='k for k in range(67, 100) if i!=k', skip_if_invalid=True)
SIL_3.w = 10
'''
input = PoissonGroup(N, rates=F)
SIL = Synapses(input, HiddenNeurons_1,'w : 1')
SIL.connect(p=1.0)
SIL.w = 1
#SIL.w = 'rand()'
'''
#Synapses Hidden Layer with STDP
SHL = Synapses(HiddenNeurons_1, HiddenNeurons_2,
             '''w : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             on_pre='''ge += w
                    Apre += dApre
                    w = clip(w + Apost, 0, gmax)''',
             on_post='''Apost += dApost
                     w = clip(w + Apre, 0, gmax)''',
             )
SHL.connect(p=1.0)
SHL.w = 'rand()* gmax'


#inputMon = StateMonitor(InputNeuron_1, variables=True, record=True)
inputSpikeMon_1 = SpikeMonitor(InputNeuron_1)
inputSpikeMon_2 = SpikeMonitor(InputNeuron_2)
inputSpikeMon_3 = SpikeMonitor(InputNeuron_3)

HiddenSpikeMon_1 = SpikeMonitor(HiddenNeurons_1)
HiddenSpikeMon_2 = SpikeMonitor(HiddenNeurons_2)

SynapsesMon = StateMonitor(SHL, 'w', record=[0, 1, 2, 3])

inputMon_1 = StateMonitor(InputNeuron_1, variables=True, record=True)
inputMon_2 = StateMonitor(InputNeuron_2, variables=True, record=True)
inputMon_3 = StateMonitor(InputNeuron_3, variables=True, record=True)

hiddenMon_1 = StateMonitor(HiddenNeurons_1, variables=True, record=True)
hiddenMon_2 = StateMonitor(HiddenNeurons_2, variables=True, record=True)

    #show()
#visualise_connectivity(SIL)
#visualise_connectivity(SHL)
##load_weight()
#visualise_connectivity(SHL)
#load_weight()
simulate_weight(5)
subplot(221)
brian_plot(HiddenSpikeMon_1)


#visualise_connectivity(SIL_1)
#brian_plot(SIL_2.w)

subplot(232)
brian_plot(SHL.w)
subplot(233)
plot(SynapsesMon.t/second, SynapsesMon.w.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(234)
brian_plot(HiddenSpikeMon_1)
subplot(235)
brian_plot(HiddenSpikeMon_2)



#print('Spike times: %s' %inputSpikeMon.t[:])
#plot(inputMon.t/ms, inputMon.v[0], label='v1')
#plot(inputMon.t/ms, inputMon.I[0], label='I1')
#for t in inputSpikeMon.t:
#   axvline(t/ms, ls='--', c='C8', lw=3)
#xlabel('Time (ms)')
#ylabel('v')
#legend(loc='best');
tight_layout()
show()