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
DAY = 22
NAME = 'simplesim2'
RANGE = range(3, 15)
who = (USER, YEAR, MONTH, DAY)

comp = partial(compare, customer=USER, year=YEAR, month=MONTH, day=DAY,
               realon=True)

start = time.time()
with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
    for i, res in zip(RANGE, executor.map(comp,RANGE)):
        with open(TMPDIR + f'{NAME}_{i}.pkl', 'wb') as fh: pickle.dump(res, fh)
end = time.time()

print(end - start)

