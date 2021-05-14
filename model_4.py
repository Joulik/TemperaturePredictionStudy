from datetime import datetime
import datetime
import pandas as pd

from model_3 import split_rescale
from model_3 import lin_reg
from model_3 import dec_tree_reg

def get_day_of_year(date):
    return (date - datetime.datetime(year=date.year,month=1,day=1)).days + 1


# read csv
arxiv_csv = 'FR000007150_daily_weather_arxiv.csv'
cols=['date','T_min','T_max','Prcp']
df_PAR = pd.read_csv(arxiv_csv,delimiter=',',names=cols,parse_dates=['date'])

temperature_type = ['T_min','T_max']

for temp in temperature_type:

    # create target dataframe
    df_target = pd.DataFrame()

    df_target[temp]=df_PAR[temp][2:]
    #print(df_features.head())

    # create features DF
    df_features = pd.DataFrame()

    df_features['day_of_year']=df_PAR['date'].apply(get_day_of_year)

    df_features['temp_date_1']=df_PAR[temp].shift(periods=1)
    df_features['temp_date_2']=df_PAR[temp].shift(periods=2)

    df_features = df_features[2:]

    # turn df into numpy arrays
    X = df_features.to_numpy()
    y = df_target.to_numpy()

    # split data and rescale features
    X_train_resc,X_test_resc,y_train,y_test = split_rescale(X,y)

    # linear regression
    score,coeffs,dist_lr = lin_reg(X_train_resc,X_test_resc,y_train,y_test)

    print("-----LINEAR REGRESSION-----")
    print("Analyzing {}".format(temp))

    print("Score: {}".format(score))
    print(df_features.columns)
    print("Coefficients: {}".format(coeffs))

    print("")
    print("Mean: {}".format(dist_lr.mean()))
    print("Stddv: {}".format(dist_lr.std()))
    print("")

    # decision tree regressor
    score,feat_imp,dist_dtr = dec_tree_reg(X_train_resc,X_test_resc,y_train,y_test)

    print("-----DECISION TREE REGRESSOR-----")

    print("Score: {}".format(score))
    print(df_features.columns)
    #print("Coefficients: {}".format(coeffs))
    print("Features importance: {}".format(feat_imp))

    print("")
    print("Mean: {}".format(dist_dtr.mean()))
    print("Stddv: {}".format(dist_dtr.std()))
    print("")

    #print(df_features.size)
    #print(df_target.size)