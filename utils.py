import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import os

os.rename('regressionModels.py', 'utils.py')

def random_forest_regressor(data, team_data):
    x_train, x_test, y_train, y_test = split_data(data, team_data)
    rfr = RandomForestRegressor(random_state=42)
    rfr.fit(x_train, y_train)
    
    y_pred = rfr.predict(x_test)
    y_pred = np.ceil(y_pred).astype(int)
    return y_test, y_pred

def linearRegression(data, team_data):
    x_train, x_test, y_train, y_test = split_data(data, team_data)
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    y_pred = np.round(y_pred).astype(int)
    return y_test, y_pred

def split_data(data, team_data):
    latest_year = data['season_end_year'].max()
    n = 5
    split_year = latest_year - n
    training_data = team_data[team_data["season_end_year"] <= split_year]
    if (team_data['team'] == 'Luton Town').any(): ##returns True or False and any() checks if any row in the series is True
        testing_data =  team_data[team_data["season_end_year"] == 2024]
    elif (team_data['team'] == 'Brentford').any():
        testing_data = team_data[team_data["season_end_year"] >= 2022]
    else:
        testing_data =  team_data[team_data["season_end_year"] > split_year]
    
    #define features

    x_train = training_data[['position']]
    x_test = testing_data[['position']]
    #define target
    y_train = training_data['position']
    y_test = testing_data[['season_end_year', 'position']]
    #convert y_test to a numpy array to later be compared to the predictions

    return x_train, x_test, y_train, y_test

def padded_test(team_df, years):
    #mearges the team data with years so the clubs with missing data for some of the years is filled with 0 (meaning not in the league)
    padded_df = years.merge(team_df, on='season_end_year', how='left') 
    padded_df.fillna({'position':0}, inplace=True)
    return padded_df