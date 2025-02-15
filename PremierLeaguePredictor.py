import pandas as pd
import regressionModels
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sqlite3
import syntheticStats as synth

n=5
filename = 'pl-tables-1993-2024.csv'
data = pd.read_csv(filename)
#team_name = input("Enter a team name: ")
#prediction_df = pd.DataFrame(columns=['team', 'predicted_position_1', 'predicted_position_2', 'predicted_position_3', 'predicted_position_4', 'predicted_position_5'])
rows = []
#predict whole table
#conver csv to an SQL table
conn = sqlite3.connect(':memory:')
data_SQL = data.to_sql("my_table", conn, index=False, if_exists='replace')

#SQL query to obtain the tables of the past 5 seasons
query_table = '''
        WITH LatestSeasons AS (
        SELECT DISTINCT season_end_year 
        FROM my_table
        ORDER BY season_end_year DESC
        LIMIT 5
    )
    SELECT season_end_year, team 
    FROM my_table
    WHERE season_end_year IN (SELECT season_end_year FROM LatestSeasons)
    ORDER BY season_end_year DESC
    '''
tables = pd.read_sql_query(query_table, conn)
conn.close()
#obtain each unique team that has been in the past 5 seasons
teams = tables["team"].unique()

#run each team through the model
for i in range (len(teams)):
    if teams[i] == 'Brentford':
        team_data = synth.brentfordStats(data, teams[i])
        y_test, y_pred = regressionModels.linearRegression(data, team_data)
    elif teams[i] == 'Luton Town':
        team_data = synth.brentfordStats(data, teams[i])
        y_test, y_pred = regressionModels.linearRegression(data, team_data)
    else:
        team_data = data[data['team'] == teams[i]]
        y_test, y_pred = regressionModels.linearRegression(data, team_data)
    new_row = {'team': teams[i], 'predicted_positions': y_pred}
    rows.append(new_row)

predictions_df = pd.DataFrame(rows)
print(predictions_df)
"""
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
"""
#PREDICT FUTURE RESULT
