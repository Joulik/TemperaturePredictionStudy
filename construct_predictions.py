from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import requests


def request_url(url):
    '''
    Args:
        url from which predictions are requested
    Output:
        list with date of prediction day, AM and PM predictions for Day+1, Day+2, ... Day+8  
    '''
    r = requests.get(url)
    status = r.status_code

    if status==200:
        print('OK')
    elif status==404:
        print("Error")
    elif status==403:
        print("Access forbidden")
    elif status==500:
        print("Internal server error")

    s = BeautifulSoup(r.content,'html.parser')

    div_pred_temp = []
    for text in s.find_all('div',{'class':'forecast-line__pictos--temp'}):
        b = text
        div_pred_temp.append(b)

    today = date.today().strftime("%d/%m/%Y")
    pred_temp = [pt.get_text() for pt in div_pred_temp][2:]
    pred_temp.insert(0,today)
    
    #print(pred_temp)
    return pred_temp

predicted_temps = request_url('https://www.meteo-paris.com/ile-de-france/previsions')

# Append daily predictions to prediction file
pd.DataFrame.from_records([predicted_temps]).to_csv('ParisMontsouris_temp_predictions.csv',index=False,mode='a',header=False)

# Append daily predictions to prediction backup file
pd.DataFrame.from_records([predicted_temps]).to_csv('backup_ParisMontsouris_temp_predictions.csv',index=False,mode='a',header=False)