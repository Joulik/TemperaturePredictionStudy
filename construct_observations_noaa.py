from datetime import datetime
import pandas as pd
import requests
import sys

def request_weather_arxiv(datatype):
  '''
  Args:
    datatype: for example, min temperature or avg temperature etc
  Output:
    Daily data for precipitations, min and max temperatures  
  '''

  dataset='GHCND'
  # location code for Paris Montsouris station
  location="GHCND:FR000007150"

  if datatype=='PRCP':
    print('===================================')
    print(' Collecting observations from NOAA')
    print(' Station: {}'.format(location))
    print('===================================')

  n_token='VMPMXiToPnVyavbJBWucazFqvkfkQnAD'

  s_date = '2021-04-01'
  e_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

  weathers_url="https://www.ncdc.noaa.gov/cdo-web/api/v2/data/"
  params='stationid=' + location + '&' 'datasetid=' + dataset + '&' + 'startdate=' + s_date + '&' + 'enddate=' + e_date + '&' + 'limit=1000' + '&' + 'units=metric' + '&datatypeid=' + datatype
  noaa_token = {'token': n_token}

  try:
    req = requests.get(weathers_url, params=params, headers=noaa_token)
    df_req = pd.DataFrame(req.json()['results'])
    #print(req.json()['results'])
  except KeyError:
    print('ERROR: No data available in date range, script stops')
    sys.exit(1)

  return pd.DataFrame(df_req,columns=['date','value'])

df_PRCP = request_weather_arxiv('PRCP')
df_TMIN = request_weather_arxiv('TMIN')
df_TMAX = request_weather_arxiv('TMAX')

df_aux = pd.merge(df_TMIN,df_TMAX,how='outer',on='date',suffixes=('_TMIN','_TMAX'))

pd.merge(df_aux,df_PRCP,how='outer',on='date',suffixes=('','_PRCP'))\
  .sort_values(by='date')\
  .to_csv('Station_observed_temp.csv',index=False,mode='w',header=False)

# Backup file
pd.merge(df_aux,df_PRCP,how='outer',on='date',suffixes=('','_PRCP'))\
  .sort_values(by='date')\
  .to_csv('backup_Station_observed_temp.csv',index=False,mode='w',header=False)  