from datetime import datetime,timedelta
from io import StringIO
import pandas as pd
import requests

def request_url(url):
    '''
    Args:
        url
    Ouput:
        Date of observation, min temperature, max temperature
    '''

    #url = 'https://static.meteo-paris.com/station/downld02.txt'
    r_data = requests.get(url)

    aux = StringIO(r_data.text)
    col_names = ['Date','Time','Temp_Out','Hi_Temp','Low_Temp','Out_Hum','Dew_Pt','Wind_Speed',
            'Wind_Dir','Wind_Run','Hi_Speed','Hi_Dir','Wind_Chill','Heat_Index','THW_Index','Bar',
            'Rain','Rain_Rate','Heat_DD','Cool_DD','In_Temp','In_Hum','In_Dew','In_Heat',
             'In_EMC','In_Air_Dens','Temp_2nd','Wind_Samp','Wind_TX','ISS_Recept','Arc_Int']

    df_list = pd.read_csv(aux,skiprows=3,delimiter="\s+",header=None,names=col_names)

    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%d/%m/%y')

    if yesterday[0]=='0':
        yesterday_updated = yesterday[1:]

    yesterday_csv = datetime.strftime(datetime.now() - timedelta(1), '%d/%m/%Y')
    t_min = df_list[df_list['Date']==yesterday_updated]['Temp_Out'].min()
    t_max = df_list[df_list['Date']==yesterday_updated]['Temp_Out'].max()

    return yesterday_csv,t_min,t_max

yesterday_date, temp_min, temp_max = request_url('https://static.meteo-paris.com/station/downld02.txt')

data=[yesterday_date,temp_min,temp_max]

# Append daily observations to observation file
pd.DataFrame.from_records([data]).to_csv('ParisMontsouris_observed_temp.csv',index=False,mode='a',header=False)

# Append daily observations to backup observation file
pd.DataFrame.from_records([data]).to_csv('backup_ParisMontsouris_observed_temp.csv',index=False,mode='a',header=False)