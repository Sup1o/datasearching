import numpy as np 
import pandas as pd
import csv

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

matches['Year']=matches['Date'].apply(lambda x : x.split('(')[0]).apply(lambda x : x.split()[-1]).astype(int)
merged_data = pd.merge(matches,cups_stats, on=['Year', 'Year'])
merged_data = merged_data[['Year','HomeTeamName','AwayTeamName','Host','HomeTeamGoals','AwayTeamGoals']]

#calculate the factorial
def factorial(n):
    factorial = 1
    if n == 0:
        factorial = 1
    else:
        for i in range (1,int(n)+1):
            factorial = int(factorial * i)
    return factorial

def Poisson_formula(k,lamda):
    e = 2.7183
    return round((pow(lamda,k)*pow(e,-lamda))/factorial(k),2)



def winner(Home_team,Away_team):
    print( '\n'+ Home_team + ' vs ' + Away_team)

    if Home_team == Away_team:
        print('They are the same team.')
    else:
        #Average number of goals scored by the home team and average number of goals conceded by the away team
        home_goal_by_all_home = 0
        for a in merged_data['HomeTeamGoals']:
            home_goal_by_all_home += a
        Avg_home_goal_of_all_team = round(home_goal_by_all_home / (merged_data.shape[0]),4)
        Avg_away_conceded_of_all_team = Avg_home_goal_of_all_team

        #Average number of goals scored by the away team and average number of goals conceded by the home team
        away_goal_by_all_away = 0
        for a in merged_data['AwayTeamGoals']:
            away_goal_by_all_away += a
        Avg_away_goal_of_all_team = round(away_goal_by_all_away / (merged_data.shape[0]),4)
        Avg_home_conceded_of_all_team = Avg_away_goal_of_all_team


        data_home = merged_data[merged_data['HomeTeamName']==Home_team]
        data_away = merged_data[merged_data['AwayTeamName']==Away_team]
        home_goal = 0
        away_goal = 0
        home_con = 0
        away_con = 0

        #calculate home team's atk and def strength
        for a in data_home['HomeTeamGoals']:
            home_goal += a 
        Avg_home_goal = round(home_goal / (data_home.shape[0]),2)
        Home_atk_strength = round(Avg_home_goal/ Avg_home_goal_of_all_team,4)

        for a in data_home['AwayTeamGoals']:
            home_con += a
        Avg_home_con = round(home_con / (data_home.shape[0]),2)
        Home_def_strength =  round(Avg_home_con/ Avg_home_conceded_of_all_team,4)



        #calculate away team's atk and def strength
        for a in data_away['AwayTeamGoals']:
            away_goal += a
        Avg_away_goal = round(away_goal / (data_away.shape[0]),2)
        Away_atk_strength =  round(Avg_away_goal/ Avg_away_goal_of_all_team,2)

        for a in data_away['HomeTeamGoals']:
            away_con += a
        Avg_away_con = round(away_con / (data_away.shape[0]),2)
        Away_def_strength =  round(Avg_away_con/ Avg_away_conceded_of_all_team,2)

        #printing some variables to check for bugs
        '''print ('Home atk strength is: ' + str(Home_atk_strength))
        print ('Away atk strength is: ' + str(Away_atk_strength))
        print ('Home def strength is: ' + str(Home_def_strength))
        print ('Away def strength is: ' + str(Away_def_strength))'''
        #expected home team goals
        Expected_home_goal = round(Home_atk_strength * Away_def_strength * Avg_home_goal_of_all_team,2)
        Expected_away_goal = round(Away_atk_strength * Home_def_strength * Avg_away_goal_of_all_team,2)

        print('Expected goal of ' + Home_team + ' is: ' + str(Expected_home_goal))
        print('Expected goal of ' + Away_team + ' is: ' + str(Expected_away_goal))

        #calculate the winning chance of home team with atmost 5 goals
        home_win_per=0
        for i in range (1,6):
            home_goal_per =  Poisson_formula(i,Expected_home_goal)
            for j in range (0,i):
                away_goal_per = Poisson_formula(j,Expected_away_goal)
                home_win_per += home_goal_per * away_goal_per
                #printing the winning percentage with the scores to check for bugs
                #print ('The percentage of ' + Home_team + ' winning with ' + str(i) + '-' + str(j) + ' over ' + Away_team + ' is: ' + str(round(home_goal_per*away_goal_per*100,2)) + '%')
        print('The probability of that the home team wins the match is: ' + str(round(home_win_per*100,2)) + '%')
        if home_win_per >= 0.5:
            print(Home_team + ' will win the match.\n')
        else:
            print(Home_team + ' will not win the match.\n')
        




def main():
    print('Exercise 6e:')

    Home_team = 'England'
    Away_team = 'Italy'
    winner(Home_team,Away_team)

    Home_team = 'France'
    Away_team = 'Germany'
    winner(Home_team,Away_team)

    Home_team = 'Netherlands'
    Away_team = 'Iceland'
    winner(Home_team,Away_team)

    Home_team = 'Spain'
    Away_team = 'Wales'
    winner(Home_team,Away_team)

    Home_team = 'Russia'
    Away_team = 'Russia'
    winner(Home_team,Away_team)

if __name__ == '__main__':
    main()