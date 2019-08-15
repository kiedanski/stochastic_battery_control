import glob
import pandas
import pickle
import numpy

from constants import *
from process_simulation import *

SIMS = ['simplesim1', 'simplesim2', 'simplesim3', 'simplesim4', 'simdays1']

for S in SIMS:
    sim1 = glob.glob(f'tmpdir/{S}*')

    res1 = []
    for fl in sim1:
        with open(fl, 'rb') as fh:
            r = pickle.load(fh)
            if len(r) > 0:
                res1.append(r)

    for pl in [objective_real, time_comp, insample_stochastic,
               distance_avg_true]:
        fig, ax = pl(res1)
        fig.savefig(IMGDIR + S + str(pl.__name__) + '.pdf')


