import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

filename = 'pl-tables-1993-2024.csv'
data = pd.read_csv(filename)
team_name = input("Enter a team name: ")

#get data of selected team
team_data = data[data['team'] == team_name]

#split the data into training and testing data
#data sorted by end year, oldest at the start
latest_year = data['season_end_year'].max()
n = 5
split_year = latest_year - n
training_data = team_data[team_data["season_end_year"] < split_year]
testing_data =  team_data[team_data["season_end_year"] > split_year]

#define features
x_train = training_data[['gd', 'points']]
x_test = testing_data[['gd', 'points']]
#define target
y_train = training_data['position']
y_test = testing_data['position']
#convert y_test to a numpy array to later be compared to the predictions
y_test = y_test.to_numpy()

#create the model and train it using linear regression
model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
#round the predictions to the nearest in as league postion cannot be a decimal
y_pred = np.ceil(y_pred).astype(int)

#calculate the accuracy of the model
#Mean Absolute Error
mae = 0
print(y_test) #DELETE IN FUTURE
print(y_pred) #DELETE IN FUTURE
for i in range(n):
    mae += abs(y_test[i] - y_pred[i])
mae = mae/n
print(f"MAE = {mae}")