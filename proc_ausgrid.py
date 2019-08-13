import pandas as pd
import datetime
import os

from constants import DATADIR, TMPDIR

RAW = DATADIR + 'ausgrid_data.csv'
raw = pd.read_csv(RAW, skiprows=1)
raw = raw.drop(['Generator Capacity', 'Postcode', 'Row Quality'], axis=1)

tmp = pd.melt(raw, id_vars=['Customer', 'Consumption Category', 'date'])

tmp =  pd.pivot_table(tmp, index=['Customer', 'date', 'variable'],
                      columns='Consumption Category', values='value')

tmp['net'] = tmp['GC'] - tmp['GG'] + tmp['CL']
datetimes = [datetime.datetime.strptime(x[1] + x[2], '%d/%m/%Y%H:%M') for x in
             tmp.index]

tmp['datetime'] = datetimes

final = tmp.reset_index()[['Customer', 'datetime', 'net']].copy()
final.columns = ['customer', 'date', 'power']

final = final.dropna(axis=0)
final = final.sort_values(['customer', 'date'])

final.to_csv(TMPDIR + 'all_customers.csv', index=None)
