# Temperature Prediction Study

When trying to predict what the minimal and maximum temperatures of a given day will be, do weather forecast specialists perform better than a model which randomly samples temperatures from 30 years of historical data for the same date?

## Requirements

- beautifulsoup

- datetime

- io

- pandas

- requests

## Construction of historical database

The database is constructed from National Oceanic and Atmospheric Administration (NOAA) data.

The NOAA API documentation can be found from https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted

The script construct_temp_prcp_database.py extracts daily minimal and maximal temperatures as well as precipitations for a user-defined range of years.

## Construction of observations file

python construct_observations.py

Observations for min and max temperatures are taken from https://static.meteo-paris.com/station/downld02.txt The script should be run everyday.

## Construction of predictions file

python construct_predictions.py

Predictions for min and max temperatures are taken from https://www.meteo-paris.com/ile-de-france/previsions The script should be run everyday.