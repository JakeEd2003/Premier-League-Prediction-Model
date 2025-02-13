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
split_year = 2019
training_data = team_data[team_data["season_end_year"] < split_year]
testing_data =  team_data[team_data["season_end_year"] > split_year]

#define features
x_train = training_data[['gd', 'points']]
x_test = testing_data[['gd', 'points']]
#define target
y_train = training_data['position']
y_test = testing_data['position']

#create the model and train it using linear regression
model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print(y_pred)