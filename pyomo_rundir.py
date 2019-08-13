import pyomo
import os
import glob
import json
import subprocess
from copy import  deepcopy
from constants import *
from mymodel import model

flist = glob.glob(RUNDIR + 'scen*.dat')

SS = 14
T = 48


solutions = []
for fl in flist:

    args = ['pyomo', 'solve', 'mymodel.py', fl, '--solver=cplex',
            '--save-results', 'results', '--results-format', 'json']

    code = subprocess.run(args)

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
    solutions.append(deepcopy(solution))


