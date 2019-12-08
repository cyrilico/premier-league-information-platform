import json
import re

def event_to_minute(game):
    for starter in game['home_team']['lineup']:
        for key in ['goals', 'own_goals', 'yellows', 'reds', 'sub_on', 'sub_off', 'missed_pens']:
            if key in starter:
                print(starter[key])
                starter[key] = list(map(lambda x: int(re.search(r'(\d+)(?:\+\d+)?', x).group(1)), map(str,starter[key])))
    for starter in game['home_team']['subs']:
        for key in ['goals', 'own_goals', 'yellows', 'reds', 'sub_on', 'sub_off', 'missed_pens']:
            if key in starter:
                starter[key] = list(map(lambda x: int(re.search(r'(\d+)(?:\+\d+)?', x).group(1)), map(str,starter[key])))
    for starter in game['away_team']['lineup']:
        for key in ['goals', 'own_goals', 'yellows', 'reds', 'sub_on', 'sub_off', 'missed_pens']:
            if key in starter:
                starter[key] = list(map(lambda x: int(re.search(r'(\d+)(?:\+\d+)?', x).group(1)), map(str,starter[key])))

    for starter in game['away_team']['subs']:
        for key in ['goals', 'own_goals', 'yellows', 'reds', 'sub_on', 'sub_off', 'missed_pens']:
            if key in starter:
                starter[key] = list(map(lambda x: int(re.search(r'(\d+)(?:\+\d+)?', x).group(1)), map(str,starter[key])))
    
    return game

for key in ['17-18','18-19']:
    games = json.load(open('{}.json'.format(key)))
    games = list(map(event_to_minute, games))
    json.dump(games, open('{}-fixed.json'.format(key), 'w'), ensure_ascii=False)