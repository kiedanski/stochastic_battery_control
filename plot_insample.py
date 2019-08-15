import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import glob
from constants import *

flist = glob.glob(TMPDIR + 'simplesim*')

pb = POWERWALL2['pb']
ps = POWERWALL2['ps']

res = {}
for fl in flist:
    with open(fl, 'rb') as fh: r = pickle.load(fh)
    if len(r) > 0:
        simnum = fl.split('/')[-1].split('_')[0][9:]
        scennum = fl.split('/')[-1].split('_')[1][:-4]
        if simnum in res:
            res[simnum][scennum] = r
        else:
            res[simnum] = {scennum: r}

def get_mpcs(x):
    smpc = {}
    smpc2 = {}
    for k, v in x.items():
        smpc_ = np.zeros(len(v))
        smpc2_ = np.zeros(len(v))

        for k1, v1 in v.items():
           aux = v1[3][2]
           w1 = aux[aux[3] == ' SecondStageCost'][5].mean()
           smpc_[int(k1) - 3] = w1
           aux = v1[4][2]
           w2 = aux[aux[3] == ' SecondStageCost'][5].mean()
           smpc2_[int(k1) - 3] = w2

        smpc[k] = smpc_
        smpc2[k] = smpc2_
    return smpc, smpc2


def plot_insample(res):
    #real = get_real_values(res)
    #donth = get_donth(res)
    smpc, smpc2 = get_mpcs(res)
    subplots_names = ['A', 'B', 'C', 'D']
    x = range(2, 14)
    fig, ax = plt.subplots(2, 2, sharex = True)
    for i in range(4):
        k = str(i + 1)
        ax_ =  ax[i // 2, i % 2]
        #ax_.plot(x, mpc[k], 'b*-', label='MPC')
        ax_.plot(x, smpc[k], 'k+-', label='SMPC')
        ax_.plot(x, smpc2[k], 'co-', label='SMPC 14')
        #ax_.axhline(y=real[k], c='g', label='Perfect Information')
        #ax_.axhline(y=donth[k], c='r', label='No battery')
        ax_.set_title('Case ' + subplots_names[i])
    handles, labels = ax[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=5)
    #fig.tight_layout()
    fig.savefig(IMGDIR + 'insample.pdf')
    return fig, ax

