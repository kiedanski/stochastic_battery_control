import numpy as np


PROJECTDIR = '/home/guso/Projects/summerschool/'

DATADIR = PROJECTDIR + 'data/'
TMPDIR = PROJECTDIR + 'tmpdir/'
RUNDIR = PROJECTDIR + 'rundir/'


PRICE_BUY_1 = np.ones(48) * 12.3
PRICE_BUY_1[14:46] = 15.8
PRICE_SELL_1 = np.ones(48) * 10


POWERWALL2 = {
    'ss'        : 1,
    'T'         : 48,
    'e_ch'      : 0.95,
    'e_dis'     : 0.95,
    'ramp_up'   : 2.5,
    'ramp_down' : -2.5,
    'b_max'     : 13.5,
    'b_min'     : 0,
    'pb'        : PRICE_BUY_1,
    'ps'        : PRICE_SELL_1
}

USERS = [2, 13, 14, 20, 33, 35, 38, 39, 56,
69, 73, 74, 75, 82, 87, 88, 101, 104,
106, 109, 110, 119, 124, 130, 137, 141, 144,
152, 153, 157, 161, 169, 176, 184, 188, 189,
193, 201, 202, 204, 206, 207, 210, 211, 212,
214, 218, 244, 246, 253, 256, 273, 276, 297]
