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

def smpc(load, real=None, bat='PW2_1', ident='sub'):
    """Runs the stochastic mpc

    :customer: TODO
    :day: TODO
    :previous: TODO
    :returns: TODO

    """
    RUNDIR_ = RUNDIR + f'{ident}/'
    os.makedirs(RUNDIR_, exist_ok=True)
    os.chdir(RUNDIR_)
    B = 0    
    xc = np.zeros(48)
    xd = np.zeros(48)
    if bat == 'PW2_1':
        PW = deepcopy(POWERWALL2)
    elif bat == 'PW2_14':
        PW = deepcopy(POWERWALL2_SS14)

    for t in range(47):
        runfiles = []
        for day, zs in load.items():
            zs_ = zs.copy()
            if real is not None:
                zs_[t] = real[t]
            out_dat = generate(**PW, b_ini=B, zs=zs_[t:])
            filename = f'scen_{day}.dat'
            with open(RUNDIR_ + filename, 'w') as fh: fh.write(out_dat)
            runfiles.append(filename)

        out_struct = generate_structure(runfiles)
        with open(RUNDIR_ + 'ScenarioStructure.dat', 'w') as fh: fh.write(out_struct)

        args = ['runef', '-m', PROJECTDIR + 'mymodel.py', '-i', RUNDIR_, '--solve',
                '--solution-writer=pyomo.pysp.plugins.csvsolutionwriter']
        with open(os.devnull, 'w') as devnull:
            subprocess.run(args, stdout=devnull)

        ef = pd.read_csv('ef.csv', header=None)
        ef_stagecost = pd.read_csv('ef_StageCostDetail.csv', header=None)
        if t == 0:
            first_cost = ef_stagecost

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
        if bat == 'PW2_14' and PW['T'] <= 14:
            PW['ss'] -= 1

    os.chdir(PROJECTDIR)
    return xc, xd, first_cost


#start = time.time()
#prev, real = init_smpc(2, dt.date(2013, 5, 23), 5)
#e1, e2 = smpc(prev)
#end = time.time() - start

#print(end)
