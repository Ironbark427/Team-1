# import dependencies
import pandas as pd

# read in csv file into dataframe
fema = pd.read_csv('DisasterDeclarationsSummaries.csv')

# drop columns that are irrelevant
fema = fema.loc[:, ['disasterNumber', 'state', 'incidentBeginDate',
                'incidentType', 'incidentEndDate']]

# create columns to link with lendingclub.com data
fema['yearBegin'] = fema['incidentBeginDate'].str[:4]
fema['monthBegin'] = fema['incidentBeginDate'].str[5:7]
fema['monthEnd'] = fema['incidentEndDate'].str[5:7]

# drop unix dates from dataframe
fema = fema.loc[:, ['disasterNumber', 'state', 'incidentType', 'yearBegin',
                'monthBegin', 'monthEnd']]

# drop all data outside of 2018
fema = fema[fema['yearBegin'] == '2018']

# drop duplicate rows with same incident named for multiple counties
fema = fema.drop_duplicates(subset=['disasterNumber'], keep=False)

# fill in all ending month with beginning month if it is missing
fema.monthEnd.fillna(fema.monthBegin, inplace=True)

# drop irrelevant disasterNumber
fema.drop(columns=['disasterNumber'], inplace=True)

# write to csv
fema.to_csv('fema_clean.csv', index=False)
