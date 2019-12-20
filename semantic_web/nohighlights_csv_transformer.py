import json
import csv

games = json.load(open('games.json'))

def no_highlights(player):
    for event in ['goals', 'own_goals', 'sub_off', 'yellows', 'reds', 'missed_pens']:
        if len(player[event]) > 0:
            return False
    return True

GAME_COUNT = 1

with open('appearances.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Player', 'Home', 'Away', 'Date', 'Team'])
    for game in games[:GAME_COUNT]:
        for team in ['home_team', 'away_team']:
                for player in game[team]['lineup']:
                    if no_highlights(player):
                        writer.writerow([player['name'], game['home_team']['name'], game['away_team']['name'], game['date'], game[team]['name']])


