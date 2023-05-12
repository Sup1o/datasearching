import numpy as np 
import pandas as pd
import csv
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD

matches = pd.read_csv('Matches.csv')  
players = pd.read_csv('Players.csv')
teams_stats = pd.read_csv('Teams stats.csv')
cups_stats=pd.read_csv('Cup stats.csv')

matches['HomeTeamName'] = matches['HomeTeamName'].apply(lambda x : x.replace(u'\xa0', u'')).apply(lambda x : x.strip())
matches['AwayTeamName'] = matches['AwayTeamName'].apply(lambda x : x.replace(u'\xa0', u'')).apply(lambda x : x.strip())

matches.replace('Soviet Union','Russia',inplace=True)
matches.replace('West Germany','Germany',inplace=True)
cups_stats.replace('Soviet Union','Russia',inplace=True)
cups_stats.replace('West Germany','Germany',inplace=True)

print('Exersise 6a.')

host_win = len(cups_stats[cups_stats.Champion == cups_stats.Host])
total_host = cups_stats.shape[0]
host_per = round((host_win/total_host)*100,2)

print('Node 1:')
Node_one = TabularCPD(  variable = 'A',
                        variable_card = 2, 
                        values = [[host_per], [100 - host_per]], 
                        evidence = ['B'], 
                        evidence_card = [1], 
                        state_names = {'A': ['Host', 'Not Host'], 'B': ['Champion']})

print(Node_one)

matches['Year']=matches['Date'].apply(lambda x : x.split('(')[0]).apply(lambda x : x.split()[-1]).astype(int)
merged_data = pd.merge(matches,cups_stats, on=['Year', 'Year'])
merged_data = merged_data[['Year','HomeTeamName','AwayTeamName','Host','HomeTeamGoals','AwayTeamGoals']]

home_win = merged_data['HomeTeamGoals']>merged_data['AwayTeamGoals']
home_name = merged_data['HomeTeamName']==merged_data['Host']
away_win = merged_data['AwayTeamGoals']>merged_data['HomeTeamGoals']
away_name = merged_data['AwayTeamName']==merged_data['Host']

merged_data['Wins']=((home_win & home_name)|(away_win & away_name))
Host_win = 0
for row in merged_data['Wins']:
    if row == True:
        Host_win += 1

Host_win_rate = round((Host_win/merged_data.shape[0])*100,2)

win = 0
played = 0
for row in teams_stats['Win']:
    win+= int(row)
for row in teams_stats['Played']:
    played+=row
win_rate = round(win/played*100,2)
print('Node 2:')
home_win_over_win = round(((win_rate-25)/Host_win_rate),2)
Node_two = TabularCPD(  variable = 'A',
                        variable_card = 1, 
                        values = [[home_win_over_win]], 
                        evidence = ['B'], 
                        evidence_card = [1], 
                        state_names = {'A': ['Home team win percent'] , 'B': ['win']}
                        )

print(Node_two)

merged_data = merged_data[['Year','HomeTeamName','AwayTeamName','Host','HomeTeamGoals','AwayTeamGoals']]

Data_2016 = merged_data[merged_data['Year']==2016]
Team_2016 = Data_2016.groupby(['HomeTeamName']).size()
Team_2016 = Team_2016.reset_index()

Team_2016.columns = ['Team','Number']
Team_2016 = Team_2016[['Team']]

for a in Data_2016['AwayTeamName']:
        existed = False
        for b in Team_2016['Team']:
            if a == b:
                existed = True
        if existed == False:
            Team_2016.loc[len(Team_2016.index)] = a

Data_before_2016 = merged_data[merged_data['Year']<2016]
Team_2016['Home Win Percent'] = 0
i = 0
for a in Team_2016['Team']:
    Host_win_rate = 0
    for b in Data_before_2016['Host']:
        if b == a:
            home_win = Data_before_2016['HomeTeamGoals']>Data_before_2016['AwayTeamGoals']
            home_name = Data_before_2016['HomeTeamName']==a
            away_win = Data_before_2016['AwayTeamGoals']>Data_before_2016['HomeTeamGoals']
            away_name = Data_before_2016['AwayTeamName']==a
            Data_before_2016['Wins']=((home_win & home_name)|(away_win & away_name))
            Host_win = 0
            for row in Data_before_2016['Wins']:
                if row == True:
                    Host_win= Host_win + 1
            Host_win_rate = round((Host_win/Data_before_2016.shape[0])*100,2)
    Team_2016.loc[i, 'Home Win Percent'] = Host_win_rate
    i += 1
Team_2016['Win Percent'] = round(25 + Team_2016['Home Win Percent']*home_win_over_win,2)
Team_2016['Champion Percent'] = 0
i = 0
for a in Team_2016['Team']:
    if a == cups_stats.at[14,'Host']:
        Team_2016.loc[i,'Champion Percent']= round(Team_2016.at[i, 'Win Percent'] * 0.7 + host_per * 0.3,2)
    else:
        Team_2016.loc[i,'Champion Percent']= round(Team_2016.at[i, 'Win Percent'] * 0.7,2)
    i += 1
print('\nProbability of winning the Euro championship of each country in 2016')
print(Team_2016)

print('\nExercise 6b. \nThe data set after hiding the columns that we ask the model(s) to predict are: \n')
Data_before_2016 = Data_before_2016[['Year','HomeTeamName','AwayTeamName','Host','HomeTeamGoals','AwayTeamGoals']]
print('\nThe Match information before 2016:\n')
print(Data_before_2016)

Team_2016 = Team_2016[['Team']]
print('\nThe Participants of EURO Championship 2016:\n')
print(Team_2016)
cups_stats = cups_stats[['Year','Host','Champion']]
print('\n The EURO Championship\'s champions and hosts stats:\n')
print(cups_stats)