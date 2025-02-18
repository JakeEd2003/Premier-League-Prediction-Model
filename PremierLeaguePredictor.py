import pandas as pd
import utils
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sqlite3
import syntheticStats as synth


n=5
filename = 'pl-tables-1993-2024.csv'
data = pd.read_csv(filename)
#team_name = input("Enter a team name: ")
#prediction_df = pd.DataFrame(columns=['team', 'predicted_position_1', 'predicted_position_2', 'predicted_position_3', 'predicted_position_4', 'predicted_position_5'])
rows = []
new_row_test = []
years = pd.DataFrame({'season_end_year': range (2020, data['season_end_year'].max()+1)})
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
        y_test, y_pred = utils.linearRegression(data, team_data)
    elif teams[i] == 'Luton Town':
        team_data = synth.brentfordStats(data, teams[i])
        y_test, y_pred = utils.linearRegression(data, team_data)
    else:
        team_data = data[data['team'] == teams[i]]
        y_test, y_pred = utils.linearRegression(data, team_data)
    new_row = {'team': teams[i], 'predicted_positions': y_pred}
    rows.append(new_row)
    #pad the test with 0's for years they werent' in the league so a table can be completed with the predictions
    y_test = utils.padded_test(y_test, years)
    y_test_rows = {'team': teams[i], '2020': y_test['position'].values[0], '2021': y_test['position'].values[1], '2022': y_test['position'].values[2], '2023': y_test['position'].values[3], '2024': y_test['position'].values[4]}
    new_row_test.append(y_test_rows)

predictions_df = pd.DataFrame(rows)
test_df = pd.DataFrame(new_row_test)
prediction_result_df = []

counter = 0
#iterate over each team
for team in teams:
    #iterate over every year predicted
    for i in range(2020, 2025):
        year = str(i) #convert year to string to be used as an index
        #check if the result for a team in a certain year in greater than 0 meaning that they participated in the league that year
        if (test_df.loc[test_df['team'] == team, year].values[0]) > 0:
            #get the list of predictions in that list saved in predictions_df
            predicted_list = predictions_df.loc[predictions_df['team'] == team, 'predicted_positions'].iloc[0]
            #get the correct value from the list for the year(the first value in the list is the fisrt year they played in the timeframe)
            val = predicted_list[counter]
            #create a row for the dataframe for the team with the prediction and relevant year
            final_df_row = {'team': team, f'{year}': val} 
            prediction_result_df.append(final_df_row)
            counter += 1
        else:
            #if team didn't play that season, place 0 for null for ease of sorting
            final_df_row = {'team': team, f'{year}': 0}
            prediction_result_df.append(final_df_row)      
    counter = 0
final = pd.DataFrame(prediction_result_df)
final = final.groupby('team', as_index=False).first()    
print(final)
"""
#get data of selected team
team_data = data[data['team'] == team_name]

#y_test, y_pred = utils.linearRegression(data, team_data)
y_test, y_pred = utils.random_forest_regressor(data, team_data)

#calculate the accuracy of the model
#Mean Absolute Error, Mean Squared Error, R2 Score
mae = mean_absolute_error(y_pred, y_test)
mse = mean_squared_error(y_pred, y_test)
r2 = r2_score(y_pred, y_test)


print(mae, mse, r2)
"""
#PREDICT FUTURE RESULT
