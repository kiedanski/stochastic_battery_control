import pandas as pd
import subprocess
import numpy as np
import os
import datetime as dt
import shutil
from write_dat_file import generate
from write_scenario_structure import generate_structure
from constants import *

def stochastic_solution():

    customer = 2
    start = dt.date(2012, 7, 10)
    days = [ start + dt.timedelta(days=n) for n in range(50)]
    #days = [x for x in days if x.weekday() == 2]
    end = days[-1]
    days = days[:-1]

    df = pd.read_csv(TMPDIR + 'all_customers.csv')
    df = df[df.customer == customer].sort_values('date')
    df['date'] = pd.to_datetime(df['date'])

    mask = df.date.between(start, end)

    df = df[mask].iloc[:-1, :]
    df['dt'] = df.date.apply(lambda x: x.date())

    try: 
        shutil.rmtree(RUNDIR)
    except FileNotFoundError as e:
        pass
    os.makedirs(RUNDIR)

    zss = []
    runfiles = []
    for d in days:
        zs = df[df.dt == d].power.values
        zss.append(zs)
        if not np.isnan(zs).any():
            out_dat = generate(**POWERWALL2, b_ini=0, zs=zs)
            filename = f'scen_{d}.dat'
            with open(RUNDIR + filename, 'w') as fh: fh.write(out_dat)
            runfiles.append(filename)


    out_struct = generate_structure(runfiles)
    with open(RUNDIR + 'ScenarioStructure.dat', 'w') as fh: fh.write(out_struct)


    args = ['runef', '-m', 'mymodel.py', '-i', RUNDIR, '--solve',
            '--solution-writer=pyomo.pysp.plugins.csvsolutionwriter']
    subprocess.run(args)

    ef = pd.read_csv('ef.csv', header=None)
    ef_stagecost = pd.read_csv('ef_StageCostDetail.csv', header=None)

    os.remove('ef.csv')
    os.remove('ef_StageCostDetail.csv')

    return ef, ef_stagecost
