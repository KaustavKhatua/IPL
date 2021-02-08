import os
os.chdir("F:\\All\\IPL")
data_source = "F:\\All\\IPL\\ipl_yaml"
data_files = os.listdir(data_source)

import pandas
match_details = pandas.DataFrame(columns = ['City', 'Venue', 'Date', 'Team 1', 'Team 2', 'Team 1 Captain', 'Team 2 Captain', 'Toss Winner', 'Decision', 'Opening Team', 'Winner', 'By Runs', 'By Wickets', 'Run Won By', 'Wickets Won By', 'Player of the Match', 'Umpire 1', 'Umpire 2'])

match_id = 0
count = 0
import yaml
for file_name in data_files:
    count = count + 1
    print(count)
#    print(file_name)
    with open(data_source+"\\"+file_name) as f:
        data = yaml.load(f)
    match_id = match_id + 1
    
    # 2020-09-20  Delhi Capitals VS Kings XI Punjab match city is not present.
    try:
        city = data['info']['city']
    except:
        city = None
    venue = data['info']['venue']
    date_played = data['info']['dates'][0]
    teams = data['info']['teams']
    team1 = teams[0]
    team2 = teams[1]
    team1_captain = None
    team2_captain = None
    toss_winner = data['info']['toss']['winner']
    decision = data['info']['toss']['decision']
    opening_team = data['innings'][0]['1st innings']['team']
    
    # Match tied cases
    try:
        winner = data['info']['outcome']['winner']
        by = data['info']['outcome']['by']
        by_runs = 0
        by_wickets = 0
        runs_won_by = None
        wickets_won_by = None
        if list(by.keys())[0] == 'runs':
            by_runs = 1
            runs_won_by = by['runs']
        else:
            by_wickets = 1
            wickets_won_by = by['wickets']
    except:
        winner = "Tied"
        by_runs = None
        by_wickets = None
        runs_won_by = None
        wickets_won_by = None
    
    # Match cancelled cases
    try:
        player_of_the_match = data['info']['player_of_match'][0]
    except:
        player_of_the_match = None
    umpires = data['info']['umpires']
    umpire1 = umpires[0]
    umpire2 = umpires[1]
# print(by.keys())
    match_details.loc[match_id] = [city, venue, date_played, team1, team2, team1_captain, team2_captain, toss_winner, decision, opening_team, winner, by_runs, by_wickets, runs_won_by, wickets_won_by, player_of_the_match, umpire1, umpire2]

print(match_details)
match_details.to_csv("MatchDetails.csv", index = False)
