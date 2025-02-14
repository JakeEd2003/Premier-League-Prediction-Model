import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import regressionModels

n=5
filename = 'pl-tables-1993-2024.csv'
data = pd.read_csv(filename)
team_name = input("Enter a team name: ")

#get data of selected team
team_data = data[data['team'] == team_name]

#y_test, y_pred = regressionModels.linearRegression(data, team_data)
y_test, y_pred = regressionModels.random_forest_regressor(data, team_data)

#calculate the accuracy of the model
#Mean Absolute Error
mae = 0
for i in range(n):
    mae += abs(y_test[i] - y_pred[i])
mae = mae/n
print(f"MAE = {mae}")

#ADD MORE ACCURACY MEASURES (MEAN SQUARED ERROR, R2)