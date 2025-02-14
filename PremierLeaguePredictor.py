import pandas as pd
import regressionModels
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

n=5
filename = 'pl-tables-1993-2024.csv'
data = pd.read_csv(filename)
team_name = input("Enter a team name: ")

#get data of selected team
team_data = data[data['team'] == team_name]

#y_test, y_pred = regressionModels.linearRegression(data, team_data)
y_test, y_pred = regressionModels.random_forest_regressor(data, team_data)

#calculate the accuracy of the model
#Mean Absolute Error, Mean Squared Error, R2 Score
mae = mean_absolute_error(y_pred, y_test)
mse = mean_squared_error(y_pred, y_test)
r2 = r2_score(y_pred, y_test)


print(mae, mse, r2)
#ADD MORE ACCURACY MEASURES (MEAN SQUARED ERROR, R2)