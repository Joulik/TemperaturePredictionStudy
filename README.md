# Temperature Prediction Study

From basic models based on random sampling to evolved ones, how do these models perform compare with weather forecast specialists when trying to predict temperatures?  

## Requirements

- beautifulsoup

- datetime

- io

- pandas

- numpy

- requests

# Data collection

## Construction of historical database

The database is constructed from National Oceanic and Atmospheric Administration (NOAA) data.

The NOAA API documentation can be found from https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted

The script construct_temp_prcp_database.py extracts daily minimal and maximal temperatures as well as precipitations for a user-defined range of years.

## Construction of observations file

python construct_observations.py

Observations for min and max temperatures starting from April, 1st 2021 are taken from NOAA database. The script should regularly be run. Unfortunately, data are sometimes missing

## Construction of predictions file

python construct_predictions.py

Predictions for min and max temperatures of Paris area are taken from https://www.meteo-paris.com/ile-de-france/previsions The script should be run everyday.

# Models

## Model 1

Predict temperatures on a given day of year by sampling these temperatures on the same day of a year chosen randomly in the preceding 40 years.

Example: min and max temperatures on April, 1st 1987 predicted from min and max temperatures on April, 1st on a year randomly sampled between 1947 and 1986.

The distribution below (bar plots) was obtained for daily predictions of min and max temperatures between 1940 and 2000 excluding leap years.

The solid lines are normal distribution functions with mean and standard deviation values obtained from the data in the bar plots. 

![figModel1](fig_model_1.png)

A possible interpretation of the plots is the following. If one attempts to predict the minimum temperature of a given day by randomly sampling the minimum temperature of this day over the previous 40 years, and if we perform this kind of prediction a large number of times, i.e. during decades, the distance between the prediction and the actual temperature will be less than 1 degree on average (low bias).

However, on average two out of three predictions will be within 5 degree of the observed temperature (high variance). This is not very useful if we want to predict whether it is going to freeze. The plot also shows that it is not rare to be wrong by 10 degrees with model 1.


## Model 2

Calculate temperatures on a given day as the mean temperatures of this day over the previous 40 years.

Example: min temperature on April, 1st 1987 calculated as the min temperature mean on April, 1st between 1947 and 1986.

The distribution below (bar plots) was obtained for daily predictions of min and max temperatures between 1940 and 2000 excluding leap years.

The solid lines are normal distribution functions with mean and standard deviation values obtained from the data in the bar plots. 

![figModel2](fig_model_2.png)

Model 2 does a slightly better job than model 1 because it yields lower variance. This observation means that the predicitions arising from model 2 on average fall closer to the observed value.

## Model 3

Model 3 is a multiple linear regression model as defined below:

![fig_MultivarLinReg](multiple_linear_regression.png)

The following four features are used to predict temperature (min and max) on a given day: temperature on the previous day (day-1), difference between temperature on day-1 and temperature on day-2, difference between temperature on day-2 and day-3, cosine and sine of the day's month.

Results obtained by means of a linear regression for model 3 are shown in the plot below. Note that a decision tree regressor model performs similarly.

![figModel3_LinReg](fig_model_3_LinReg.png)

Analysis of the features weights shows that temperature on day-1 plays a major role (see Model 5 below). In fact, this weight is more than one order of magnitude larger than the other features' weights.

## Model 4

Model 4 is like model 3 a multiple linear regression model.

Model 4 has three features, namely the day of year number (e.g. 32 for Feb. 2nd), temperature on day-1 and temperature on day-2.

The figure below shows how model 4 performs.

![figModel4_LinReg](fig_model_4_LinReg.png)

Given the results obtained with model 3, temperature on day-1 quite unsurprisingly has a weight more than one order of magnitude larger than the weight of the other features. Note that the linear regression approach yields values for mean and standard deviation equal to the decision tree regressor.

## Model 5

According to model 5 the following day temperatures is taken as the current day's temperatures.

Example: min temperature for April, 2nd 1987 is taken as min temperature on April, 1st 1987.

The solid lines are normal distribution functions with mean and standard deviation values obtained from the data in the bar plots. 

![figModel5](fig_model_5.png)

This model is perhaps the simplest one can think of to predict the following day's temperatures. Nevertheless, it performs better than model 1 and model 2. On average, the predicted value falls within less than 0.1°C from the actual temperature.