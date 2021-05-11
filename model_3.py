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

# read csv
arxiv_csv = 'FR000007150_daily_weather_arxiv.csv'
cols=['date','T_min','T_max','Prcp']
df_PAR = pd.read_csv(arxiv_csv,delimiter=',',names=cols,parse_dates=['date'])

temperature = 'T_min'

# create features dataframe
df_features = pd.DataFrame()

df_features[temperature]=df_PAR[temperature]

df_features['delta_date_1']=df_PAR[temperature].diff(1)
df_features['delta_date_2']=df_PAR[temperature].diff(2)

# month cosine and sine as features
cos_month = df_PAR['date'].dt.month.apply(cos_m)
sin_month = df_PAR['date'].dt.month.apply(sin_m)

df_features['cos_month']=cos_month
df_features['sin_month']=sin_month

df_features=df_features.dropna()
df_features=df_features[:-1]

print(df_features.size)

# create targets dataframe
df_targets = df_PAR[temperature][3:]

#print(df_targets.size)

# turn df into numpy arrays
X = df_features.to_numpy()
y = df_targets.to_numpy()

# data splitting
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)

# feature scaling
scaler = StandardScaler()
scaler.fit(X_train)

X_train_resc = scaler.transform(X_train)
X_test_resc = scaler.transform(X_test)

# linear regression
reg_all = LinearRegression()
reg_all.fit(X_train_resc, y_train)
y_pred = reg_all.predict(X_test_resc)

dist = y_test - y_pred
print(dist.mean())
print(dist.std())

print(reg_all.score(X_test_resc,y_test))
print(df_features.columns)
print(reg_all.coef_)

#viz(dist,dist)

#plt.hist(dist,bins=41)
#plt.xlim((-20,20))
#plt.show()


# decision tree regressor
reg_dtr = DecisionTreeRegressor(max_depth=10)
reg_dtr.fit(X_train_resc, y_train)
y_pred = reg_dtr.predict(X_test_resc)

dist = y_test - y_pred
print(dist.mean())
print(dist.std())
print(reg_dtr.feature_importances_)

#plt.hist(dist,bins=41)
#plt.xlim((-20,20))
#plt.show()
