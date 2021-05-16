from datetime import datetime
import numpy as np
import pandas as pd
import random
from viz_plotly import viz

def get_ref_temp(ref_year,ref_day,df_PAR):
    '''
    Returns min and max temperatures of a given day
    Args:
        year(int)
        day(int)
    Return:
        temp_min(float)
        Temp_max(float)
    '''    
    #construct ref_date string
    ref_year = str(ref_year)
    ref_day = str(ref_day)
    ref_date = datetime.strptime(ref_year + "-" + ref_day, "%Y-%j").strftime("%Y-%m-%d")
    ref_date = ref_date + "T00:00:00"
    
    #subset on given date
    mask = df_PAR['date']==ref_date
    
    #get T_min and T_max values
    ref_temp_min = df_PAR[mask]['T_min'].values[0]
    ref_temp_max = df_PAR[mask]['T_max'].values[0] 
    
    return ref_date,ref_temp_min,ref_temp_max
    

def get_random_temp(input_year,input_day,df_PAR):
    
    #rndm_year = random.randint(int(input_year)-40,int(input_year)-1)
    rndm_year = 0
    rndm_day = input_day

    while rndm_year%4 == 0:
        rndm_year = random.randint(int(input_year)-40,int(input_year)-1)
            
    rndm_year = str(rndm_year)
    rndm_day = str(rndm_day)

    rndm_date = datetime.strptime(rndm_year + "-" + rndm_day, "%Y-%j").strftime("%Y-%m-%d")
    rndm_date = rndm_date + "T00:00:00"

    date, rndm_T_min, rndm_T_max = get_ref_temp(rndm_year,rndm_day,df_PAR)

    return rndm_T_min,rndm_T_max


def run_model_1():
    # model 1
    print("Working with model 1")
    # read arxiv CSV file
    arxiv_csv = 'FR000007150_daily_weather_arxiv.csv'
    print("Analyzing {}".format(arxiv_csv))
    cols=['date','T_min','T_max','Prcp']
    df_PAR = pd.read_csv(arxiv_csv,delimiter=',',names=cols)

    # generate list of years to sample, avoid leap years
    year_list=[]
    for y in range(1940,2001):
        if y%4 != 0:
            year_list.append(y)

    list_T_min = []
    list_T_max = []
    for y in year_list:
        for d in range(1,366):
            
            # get min and max temperatures for day d of year y
            date, actual_T_min, actual_T_max = get_ref_temp(y,d,df_PAR)
             
            # get min and max temperatures for day d of
            # year randomly sampled from previous year_span years     
            rndm_T_min, rndm_T_max = get_random_temp(y,d,df_PAR)
            
            # calculate distance between randomly sampled temps
            # and actual temps    
            dist_T_min = actual_T_min - rndm_T_min
            dist_T_max = actual_T_max - rndm_T_max

            # update list of distances    
            list_T_min.append(dist_T_min)
            list_T_max.append(dist_T_max)
        
            #print("date: {} random date: {}".format(dt,rndm_dt))

        print("Year: {}".format(y),end='\r')
        
    # turn lists into arrays for visualization with plotly
    arr_T_min = np.array(list_T_min)
    arr_T_max = np.array(list_T_max)

    # calculate mean and std dev of distributions
    print("Mean T_min: {}".format(np.mean(list_T_min)))
    print("Stdv T_min: {}".format(np.std(list_T_min)))

    print("Mean T_max: {}".format(np.mean(list_T_max)))
    print("Stdv T_max: {}".format(np.std(list_T_max)))

    return arr_T_min,arr_T_max

if __name__=='__main__':
    arr_T_min,arr_T_max = run_model_1()
    viz(arr_T_min,arr_T_max)
