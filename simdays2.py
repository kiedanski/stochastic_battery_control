from compare_mpcs import compare
import time
import pickle
from constants import *
from functools import partial
import concurrent.futures
import shutil
import os

try:
    shutil.rmtree(RUNDIR)
except:
    pass

os.makedirs(RUNDIR, exist_ok=True)


USER = 300
YEAR = 2013
MONTH = 5
DAY = 15
NAME = 'simdays2'
RANGE = range(2, 10)
who = (USER, YEAR, MONTH, DAY)

def comp_(d, l, u, y, m, r):
    return compare(l, u, y, m, d, r)


comp = partial(comp_, l=10, u=USER, y=YEAR, m=MONTH, r=True)


start = time.time()
with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
    for i, res in zip(RANGE, executor.map(comp,RANGE)):
        with open(TMPDIR + f'{NAME}_{i}.pkl', 'wb') as fh: pickle.dump(res, fh)
end = time.time()

print(end - start)

