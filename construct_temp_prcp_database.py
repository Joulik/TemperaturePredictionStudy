import pandas as pd
import requests

def request_weather_arxiv(datatype,year):
  '''
  Args:
    datatype: for example min temperature or avg temperature etc
    year
  Output:
    Daily data for min and max temperatures and precipitations 
  '''

  dataset='GHCND'
  # location code for Paris Montsouris station
  location="GHCND:FR000007150"

  if datatype=='PRCP':
    print('=============================')
    print(' Station: {}'.format(location))
    print('=============================')
    
  n_token='VMPMXiToPnVyavbJBWucazFqvkfkQnAD'

  s_date = str(year) + '-01-01'
  e_date = str(year) + '-12-31'

  weathers_url="https://www.ncdc.noaa.gov/cdo-web/api/v2/data/"
  params='stationid=' + location + '&' 'datasetid=' + dataset + '&' + 'startdate=' + s_date + '&' + 'enddate=' + e_date + '&' + 'limit=1000' + '&' + 'units=metric' + '&datatypeid=' + datatype
  noaa_token = {'token': n_token}

  req = requests.get(weathers_url, params=params, headers=noaa_token)
  #print(req.json())
  df_req = pd.DataFrame(req.json()['results'])
      
  return pd.DataFrame(df_req,columns=['date','value'])

for year in range(2004,2021):
    df_PRCP = request_weather_arxiv('PRCP',year)
    df_TMIN = request_weather_arxiv('TMIN',year)
    df_TMAX = request_weather_arxiv('TMAX',year)
    
    df_aux=pd.merge(df_TMIN,df_TMAX,how='outer',on='date',suffixes=('_TMIN','_TMAX'))
    
    pd.merge(df_aux,df_PRCP,how='outer',on='date',suffixes=('','_PRCP'))\
      .sort_values(by='date')\
      .to_csv('Station_weather_arxiv.csv',index=False,mode='a',header=False)
    
    print('Year {}: DONE'.format(year),end='\r')