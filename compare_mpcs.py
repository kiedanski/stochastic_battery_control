from smpc import smpc, init_smpc
from pyomo_mpc import mpc
from copy import deepcopy
import subprocess
import datetime as dt
import time
import pandas as pd
import numpy as np
import os
import shutil
import json
from constants import *
from write_dat_file import generate

def eval_solution(xc, xd, load, pb, ps, e_ch, e_dis, T):
    price = 0
    for t in range(T):
        tmp = xc[t] / e_ch - xd[t] * e_dis + load[t]
        if tmp > 0:
            price += tmp * pb[t]
        else:
            price += tmp * ps[t]

    return price

def compare(customer, year, month, day, length, realon=False):

    T = 48

    prev, real = init_smpc(customer, dt.date(year, month, day), length)
    baddata = np.array([np.isnan(x).any() or len(x) == 0 for k, x in
                       prev.items()]).any()
    if baddata:
        print('Data range does not work')
    else:

        realdata = real.copy() if realon else None

        avgpast = np.mean([x for x in prev.values()], axis=0)

        res_mpc = mpc(avgpast, realdata)

        res_smpc = smpc(prev, realdata)

        gap = res_smpc[0].sum() - res_smpc[1].sum()
        if gap > 0:
            res_smpc[1][-1] = gap

        PW = deepcopy(POWERWALL2)
        out_dat = generate(**PW, b_ini=0, zs=real)
        filename = f'scen_real.dat'
        with open(RUNDIR + filename, 'w') as fh: fh.write(out_dat)

        args = ['pyomo', 'solve', 'mymodel.py', RUNDIR + filename, '--solver=cplex',
                '--save-results', 'results', '--results-format', 'json']

        with open(os.devnull, 'w') as devnull:
            subprocess.run(args, stdout=devnull)

        with open('results', 'rb') as fh: f = json.load(fh)
        os.remove('results')

        solution = {
            'ts' : np.zeros(T),
            'xc' : np.zeros(T),
            'xd' : np.zeros(T),
            'obj': 0
        }

        for k, v in f['Solution'][1]['Variable'].items():
            which = k[:2]
            num = int(k[4:-1])
            val = v['Value']
            solution[which][num] = val

        solution['obj'] = f['Solution'][1]['Objective']['obj']['Value']

        obj_true = eval_solution(solution['xc'], solution['xd'], real, POWERWALL2['pb'],
                                POWERWALL2['ps'], POWERWALL2['e_ch'],
                                POWERWALL2['e_dis'], T)

        obj_mpc = eval_solution(res_mpc[0], res_mpc[1], real, POWERWALL2['pb'],
                                POWERWALL2['ps'], POWERWALL2['e_ch'],
                                POWERWALL2['e_dis'], T)

        obj_smpc = eval_solution(res_smpc[0], res_smpc[1], real, POWERWALL2['pb'],
                                POWERWALL2['ps'], POWERWALL2['e_ch'],
                                POWERWALL2['e_dis'], T)

    return solution, res_mpc, res_smpc, obj_mpc, obj_smpc

