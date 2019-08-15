import pyomo
import numpy as np
import os
import glob
import json
import subprocess
import shutil
from copy import  deepcopy
from constants import *
from mymodel import model
from write_dat_file import generate

def mpc(caca, real=None, ident='sub'):

    RUNDIR_ = RUNDIR + f'{ident}/'
    os.makedirs(RUNDIR_, exist_ok=True)
    os.chdir(RUNDIR_)
    PW = deepcopy(POWERWALL2)
    B = 0
    xc = np.zeros(48)
    xd = np.zeros(48)
    for tt in range(48):
        zs_ = caca.copy()
        if real is not None:
            zs_[tt] = real[tt]
        out_dat = generate(**PW, b_ini=B, zs=zs_[tt:])
        filename = f't{tt}_scen_mpc.dat'
        with open(RUNDIR_ + filename, 'w') as fh: fh.write(out_dat)
        args = ['pyomo', 'solve', PROJECTDIR + 'mymodel.py', RUNDIR_ + filename, '--solver=cplex',
                '--save-results', f'{ident}t{tt}_results', '--results-format', 'json']
        with open(os.devnull, 'w') as devnull:
            code = subprocess.run(args, stdout=devnull)

        with open(f'{ident}t{tt}_results', 'rb') as fh: f = json.load(fh)
        os.remove(f'{ident}t{tt}_results')
        try:
            XC = f['Solution'][1]['Variable']['xcf[0]']['Value']
        except KeyError as e:
            XC = 0
        try:
            XD = f['Solution'][1]['Variable']['xdf[0]']['Value']
        except KeyError as e:
            XD = 0
        B += XC - XD
        xc[tt] = XC
        xd[tt] = XD
 
        PW['pb'] = PW['pb'][1:]
        PW['ps'] = PW['ps'][1:]
        PW['T'] -= 1
    os.chdir(RUNDIR)
    return xc, xd
