import json
import csv

games = json.load(open('games.json'))

translation = {
    'goals': 'Goal',
    'own_goals': 'Own_Goal',
    'sub_off': 'Substitution_Off',
    'sub_on': 'Substitution_On',
    'yellows': 'Yellow_Card',
    'reds': 'Red_Card',
    'missed_pens': 'Missed_Penalty'
}

GAME_COUNT = 380

with open('exhibitions.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Player', 'Home', 'Away', 'Date', 'Team', 'Type', 'Minute'])
    for game in games[:GAME_COUNT]:
        d,m,y = game['date'].split('/')
        game['date'] = '{}-{}-{}'.format(y,m,d)
        for team in ['home_team', 'away_team']:
            for squad in ['lineup', 'subs']:
                for player in game[team][squad]:
                    if squad == 'lineup' or len(player['sub_on']) > 0: #Do not process unused subs
                        for event in ['goals', 'own_goals', 'sub_off', 'yellows', 'reds', 'missed_pens', 'sub_on']:
                            if event in player: #sub_on not present in lineup players
                                for minute in player[event]:
                                    writer.writerow([player['name'], game['home_team']['name'], game['away_team']['name'], game['date'], game[team]['name'], translation[event], minute])


