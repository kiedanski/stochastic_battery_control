import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from constants import *

#files = [f'simplesim1_{d}.pkl' for d in range(3, 15)]

#results = []
#for f in files:
#    with open(TMPDIR + f, 'rb') as fh: results.append(pickle.load(fh))


def objective_real(res):
    real = res[0][1]['obj']
    donth = 0
    pb = POWERWALL2['pb']
    ps = POWERWALL2['ps']
    r = res[0][0]
    for i in range(48):
        donth += r[i] * pb[i] if r[i] > 0 else r[i] * ps[i] 
    N = len(res)

    mpc = np.zeros(N)
    smpc = np.zeros(N)
    smpc14 = np.zeros(N)

    for i, r in enumerate(res):
        mpc[i] = r[5]
        smpc[i] = r[6]
        smpc14[i] = r[7]

    fig, ax = plt.subplots()
    ax.plot(mpc, label='MPC')
    ax.plot(smpc, label='SMPC')
    ax.plot(smpc14, label='SMPC Long First Stage')
    ax.axhline(real, label='Perfect Information Cost', c='g')
    ax.axhline(donth, label='Do nothing cost', c='r')
    ax.legend()
    ax.set_title('Objective in the real data')
    ax.set_xlabel('Scenarios')
    ax.set_ylabel('Euro (cents)')

    return fig, ax

def time_comp(res):
    N = len(res)

    mpc = np.zeros(N)
    smpc = np.zeros(N)
    smpc14 = np.zeros(N)

    for i, r in enumerate(res):
        mpc[i] = r[8]
        smpc[i] = r[9]
        smpc14[i] = r[10]

    fig, ax = plt.subplots()
    ax.plot(mpc, label='MPC')
    ax.plot(smpc, label='SMPC')
    ax.plot(smpc14, label='SMPC Long First Stage')
    ax.legend()
    ax.set_title('Elpased time for each algorithm')
    ax.set_xlabel('Scenarios')
    ax.set_ylabel('Time')

    return fig, ax

def insample_stochastic(res): 
    N = len(res)
    smpc = np.zeros(N)
    smpc14 = np.zeros(N)
    for i, r in enumerate(res):
        aux = r[3][2]
        smpc[i] = aux[aux[3] == ' SecondStageCost'][5].mean() 
        aux = r[4][2]
        smpc14[i] = aux[aux[3] == ' SecondStageCost'][5].mean() 

    fig, ax = plt.subplots()
    ax.plot(smpc)
    ax.plot(smpc14)

    return fig, ax

def nrmse(true, aprox):
    mean = true.mean()
    nrmse_ = (true - aprox) / true.mean()
    nrmse_ = nrmse_ ** 2
    nrmse_ = nrmse_.sum() / len(true)
    nrmse_ = np.sqrt(nrmse_)
    return nrmse_


def distance_avg_true(res):
    
    dist = []
    true = res[0][0]
    aprox = res[-1][-1]
    for r in res:
        avgpast = np.mean([x for x in r[-1].values()], axis=0)
        d_ = nrmse(true, avgpast)
        dist.append(d_)

    dist = np.array(dist)
    fig, ax = plt.subplots()
    M = dist.max() * 1.1
    m = dist.min() * 0.9
    ax.plot(dist)
    ax.set_ylim([m, M])
    ax.set_xlabel('Scenarios')
    ax.set_ylabel('NRMSE')
    ax.set_title('Evolution of distance of true versus forecast')
    return fig, ax
