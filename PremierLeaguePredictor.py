import pandas as pd
import numpy as np

filename = 'pl-tables-1993-2024.csv'
data = pd.read_csv(filename)

#split the data into training and testing data
#data sorted by end year, oldest at the start
split_year = 2019
training_data = data[data["season_end_year"] < split_year]
testing_data =  data[data["season_end_year"] > split_year]