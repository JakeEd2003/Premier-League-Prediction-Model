import pandas as pd

##READ##
# This is for creating synthetic data for clubs that have not been in the Premier League long enough to have enough data, at this point in time this is Brentford and Luton town

def brentfordStats(data, name):
    lastYear = 2024
    start = 2018
    brighton_df = pd.DataFrame()
    sheffield_df = pd.DataFrame()
    brentford_df = pd.DataFrame()
    luton_df = pd.DataFrame()
    #Get data for Brighton and Sheffield Utd, as well as for Brentford or Luton depending on who's data you are looking for
    for i in range(start, lastYear+1):
        #Brighton's data from 2018 - 2020
        if i == 2018 or i == 2019 or i == 2020:
            fileterd_data = data[(data['team'] == 'Brighton') & (data['season_end_year'] == i)]
            brighton_df = pd.concat([brighton_df, fileterd_data], ignore_index=True)
        #Sheffield Utd's data from 2021 season and from past (not including 2018-20)
        elif i == 2021:
            fileterd_data = data[(data['team'] == 'Sheffield Utd') & (data['season_end_year'] < 2018)]
            sheffield_df = pd.concat([sheffield_df, fileterd_data], ignore_index=True)
            fileterd_data = data[(data['team'] == 'Sheffield Utd') & (data['season_end_year'] == i)]
            sheffield_df = pd.concat([sheffield_df, fileterd_data], ignore_index=True)
        #brentford
        else:
            #luton needs to include the data of brentford to as they only have 1 year of data
            if name == 'Luton Town' and i <= 2024:
                if i < 2024:
                    fileterd_data = data[(data['team'] == 'Brentford') & (data['season_end_year'] == i)]
                    brentford_df = pd.concat([brentford_df, fileterd_data], ignore_index=True)
                else:
                    fileterd_data = data[(data['team'] == 'Luton Town') & (data['season_end_year'] == i)]
                    luton_df = pd.concat([luton_df, fileterd_data], ignore_index=True)
            else:
                #get Brentfords 3 years of data
                fileterd_data = data[(data['team'] == 'Brentford') & (data['season_end_year'] == i)]
                brentford_df = pd.concat([brentford_df, fileterd_data], ignore_index=True)


    #combine the data for the team being processed
    if name == 'Brentford':
        synth_brent = pd.concat([brighton_df, sheffield_df, brentford_df])
    else:
        synth_brent = pd.concat([brighton_df, sheffield_df, brentford_df, luton_df])

    #order by year and change the names to the team being processed
    synth_brent = synth_brent.sort_values(by='season_end_year', ascending=True)
    synth_brent['team'] = synth_brent['team'].replace('Brighton', name)
    synth_brent['team'] = synth_brent['team'].replace('Sheffield Utd', name)
    if name == 'Luton Town':
        synth_brent['team'] = synth_brent['team'].replace('Brentford', name)
    return synth_brent