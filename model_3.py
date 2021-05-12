from datetime import datetime
import math
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

from viz_plotly import viz

def cos_m(row):
    '''
    Perform row-wise calculation of month cosine
    Arg: row(DataSeries)
    Returns: cosine of month(DataSeries)
    '''
    angle = (row - 1)/12 * 2 * math.pi
    return math.cos(angle)

def sin_m(row):
    '''
    Perform row-wise calculation of month sine
    Arg: row(DataSeries)
    Returns: sine of month(DataSeries)
    '''
    angle = (row - 1)/12 * 2 * math.pi
    return math.sin(angle)

def split_rescale(X,y):
    '''
    Split data set in train and test subsets
    Args:
        X array of features (numpy array)
        y array of targets (numpy array)
    Returns:
        X_train_resc, X_test_resc rescaled features arrays (numpy arrays)
        y_train, y_test rescaled target arrays (numpy arrays)

    '''
    # data splitting
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)

    # feature scaling
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train_resc = scaler.transform(X_train)
    X_test_resc = scaler.transform(X_test)

    return X_train_resc,X_test_resc,y_train,y_test

def lin_reg(X_train_res,X_test_resc,y_train,y_test):
    '''
    Linear regression
    Args:
        X_train_res,X_test_resc,y_train,y_test (numpy arrays)
    Returns:
        score (float)
        coeffs (array)
        diff (numpy array)
    '''
    reg_lin = LinearRegression()
    reg_lin.fit(X_train_resc, y_train)
    y_pred = reg_lin.predict(X_test_resc)

    dist = y_test - y_pred
    
    score = reg_lin.score(X_test_resc,y_test)
    coeffs = reg_lin.coef_

    return score,coeffs,dist

def dec_tree_reg(X_train_resc,X_test_resc,y_train,y_test):
    '''
    Decision Tree Regressor
    Args:
        X_train_res,X_test_resc,y_train,y_test (numpy arrays)
    Returns:
        score (float)
        coeffs (array)
        diff (numpy array)
    '''

    reg_dtr = DecisionTreeRegressor(max_depth=10)
    reg_dtr.fit(X_train_resc, y_train)
    y_pred = reg_dtr.predict(X_test_resc)

    dist = y_test - y_pred
    
    score = reg_dtr.score(X_test_resc,y_test)
    feat_imp = reg_dtr.feature_importances_

    return score,feat_imp,dist


# read csv
arxiv_csv = 'FR000007150_daily_weather_arxiv.csv'
cols=['date','T_min','T_max','Prcp']
df_PAR = pd.read_csv(arxiv_csv,delimiter=',',names=cols,parse_dates=['date'])

temperature_type = ['T_min','T_max']

for temp in temperature_type:

    # create features dataframe
    df_features = pd.DataFrame()

    df_features[temp]=df_PAR[temp]

    df_features['delta_date_1']=df_PAR[temp].diff(1)
    df_features['delta_date_2']=df_PAR[temp].diff(2)

    # month cosine and sine as features
    cos_month = df_PAR['date'].dt.month.apply(cos_m)
    sin_month = df_PAR['date'].dt.month.apply(sin_m)

    df_features['cos_month']=cos_month
    df_features['sin_month']=sin_month

    df_features=df_features.dropna()
    df_features=df_features[:-1]

    print("Size of features DF: {}".format(df_features.size))

    # create targets dataframe
    df_targets = df_PAR[temp][3:]
    #print(df_targets.size)

    # turn df into numpy arrays
    X = df_features.to_numpy()
    y = df_targets.to_numpy()

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

    if temp=='T_min':
        arr_T_min_lr  = dist_lr
        arr_T_min_dtr = dist_dtr
    else:
        arr_T_max_lr = dist_lr
        arr_T_max_dtr = dist_dtr

viz(arr_T_min_lr, arr_T_max_lr)
viz(arr_T_min_dtr,arr_T_max_dtr)

#plt.hist(dist,bins=41)
#plt.xlim((-20,20))
#plt.show()