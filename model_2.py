from model_1 import get_ref_temp
from datetime import datetime
import numpy as np
import pandas as pd
from viz_plotly import viz

# def get_ref_temp(ref_year,ref_day,df_PAR):
#     '''
#     Returns min and max temperatures of a given day
#     Args:
#         year(int)
#         day(int)
#     Return:
#         temp_min(float)
#         Temp_max(float)
#     '''    
#     #construct ref_date string
#     ref_year = str(ref_year)
#     ref_day = str(ref_day)
#     ref_date = datetime.strptime(ref_year + "-" + ref_day, "%Y-%j").strftime("%Y-%m-%d")
#     ref_date = ref_date + "T00:00:00"
    
#     #subset on given date
#     mask = df_PAR['date']==ref_date
    
#     #get T_min and T_max values
#     ref_temp_min = df_PAR[mask]['T_min'].values[0]
#     ref_temp_max = df_PAR[mask]['T_max'].values[0] 
    
#     return ref_date,ref_temp_min,ref_temp_max
    
    
def get_hist_temp(date,year_span,df_PAR):
    '''
    Returns min and max temperature for a given day averaged over year_span years
    Args:
        date(datetime obj)
        year_span(int)
    Returns
        mean T_min(float)
        mean T_max(float)
    
    '''
    
    test_date = datetime.strptime(date,"%Y-%m-%d" + "T" + "%H:%M:%S")
    test_year = test_date.year
    #print(test_year)
    
    test_year_start = test_year - year_span
    test_year_end = test_year - 1
    
    test_day = test_date.day
    test_month = test_date.month
    #print(test_day,test_month)
    
    mask_d = df_PAR['date'].dt.day == test_day
    mask_m = df_PAR['date'].dt.month == test_month
    mask_y_start = df_PAR['date'].dt.year >= test_year_start 
    mask_y_end = df_PAR['date'].dt.year <= test_year_end
    
    mask = mask_d & mask_m & mask_y_start & mask_y_end
    
    return df_PAR[mask]['T_min'].mean(),df_PAR[mask]['T_max'].mean()


def run_model_2():
    # model 2
    print("Working with model 2")
    # read arxiv CSV file
    arxiv_csv = 'FR000007150_daily_weather_arxiv.csv'
    print("Analyzing {}".format(arxiv_csv))
    cols=['date','T_min','T_max','Prcp']
    df_PAR = pd.read_csv(arxiv_csv,delimiter=',',names=cols,parse_dates=['date'])

    #construct list of years for historical analysis excluding leap years
    year_list=[]
    for y in range(1940,1970):
        if y%4 != 0:
            year_list.append(y)
        
    #initialize lists for results        
    list_T_min = []
    list_T_max = []
    for y in year_list:
        for d in range(1,366):
        
            #get reference temperatures
            date, actual_T_min, actual_T_max = get_ref_temp(y,d,df_PAR)
            #print(date,actual_T_min,actual_T_max)

            #get historical mean temperatures on date over year_span years
            hist_avg_T_min, hist_avg_T_max = get_hist_temp(date,40,df_PAR)
        
            #calculate distance between actual and average historical
            dist_T_min = actual_T_min - hist_avg_T_min
            dist_T_max = actual_T_max - hist_avg_T_max
        
            list_T_min.append(dist_T_min)
            list_T_max.append(dist_T_max)

        print("Year: {}".format(y),end='\r')
        
    arr_T_min = np.array(list_T_min)
    arr_T_max = np.array(list_T_max)

    print("Mean T_min: {}".format(np.mean(list_T_min)))
    print("Stdv T_min: {}".format(np.std(list_T_min)))

    print("Mean T_max: {}".format(np.mean(list_T_max)))
    print("Stdv T_max: {}".format(np.std(list_T_max)))

    return arr_T_min,arr_T_max

if __name__=='__main__':
    arr_T_min,arr_T_max = run_model_2()
    viz(arr_T_min,arr_T_max)