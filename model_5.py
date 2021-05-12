# from datetime import datetime
# import math
import numpy as np
import pandas as pd
from viz_plotly import viz

# read csv
arxiv_csv = 'FR000007150_daily_weather_arxiv.csv'
cols=['date','T_min','T_max','Prcp']
df_PAR = pd.read_csv(arxiv_csv,delimiter=',',names=cols,parse_dates=['date'])

n = df_PAR['T_min'].size

temperature_types = ['T_min','T_max']

for temp in temperature_types:

    observed  = df_PAR[temp][1:n].to_numpy()
    predicted = df_PAR[temp][0:n-1].to_numpy()

    dist = observed - predicted

    if temp=='T_min':
        arr_T_min = dist
    else:
        arr_T_max = dist

viz(arr_T_min,arr_T_max)