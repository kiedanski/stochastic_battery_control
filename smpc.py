import pandas as pd
import time
import subprocess
import numpy as np
import os
import datetime as dt
from copy import deepcopy
import shutil
from write_dat_file import generate
from write_scenario_structure import generate_structure
from constants import *



def init_smpc(customer, day, previous):

    days = [day - dt.timedelta(days=7 * n) for n in range(1, previous)]

    df = pd.read_csv(TMPDIR + 'all_customers.csv')
    df = df[df.customer == customer].sort_values('date')
    df['date'] = pd.to_datetime(df['date'])
    df['dt'] = df.date.apply(lambda x: str(x.date()))
 
    demand = {}
    for d in days:
        zs = df[df.dt == str(d)].power.values
        demand[str(d)] = deepcopy(zs)
    dayload = df[df.dt == str(day)].power.values
    return demand, dayload

def smpc(load, real=None):
    """Runs the stochastic mpc

    :customer: TODO
    :day: TODO
    :previous: TODO
    :returns: TODO

    """
    B = 0    
    xc = np.zeros(48)
    xd = np.zeros(48)
    PW = deepcopy(POWERWALL2)
    for t in range(47):
        runfiles = []
        for day, zs in load.items():
            zs_ = zs.copy()
            if real is not None:
                zs_[t] = real[t]
            out_dat = generate(**PW, b_ini=B, zs=zs_[t:])
            filename = f'scen_{day}.dat'
            with open(RUNDIR + filename, 'w') as fh: fh.write(out_dat)
            runfiles.append(filename)

        out_struct = generate_structure(runfiles)
        with open(RUNDIR + 'ScenarioStructure.dat', 'w') as fh: fh.write(out_struct)

        args = ['runef', '-m', 'mymodel.py', '-i', RUNDIR, '--solve',
                '--solution-writer=pyomo.pysp.plugins.csvsolutionwriter']
        with open(os.devnull, 'w') as devnull:
            subprocess.run(args, stdout=devnull)

        ef = pd.read_csv('ef.csv', header=None)
        ef_stagecost = pd.read_csv('ef_StageCostDetail.csv', header=None)

        os.remove('ef.csv')
        os.remove('ef_StageCostDetail.csv')
        XC = ef[(ef[2] == ' xcf') & (ef[3] == 0)][4].values[0]
        XD = ef[(ef[2] == ' xdf') & (ef[3] == 0)][4].values[0]
        B += XC - XD
        xc[t] = XC
        xd[t] = XD

        PW['pb'] = PW['pb'][1:]
        PW['ps'] = PW['ps'][1:]
        PW['T'] -= 1
    return xc, xd


#start = time.time()
#prev, real = init_smpc(2, dt.date(2013, 5, 23), 5)
#e1, e2 = smpc(prev)
#end = time.time() - start

#print(end)
