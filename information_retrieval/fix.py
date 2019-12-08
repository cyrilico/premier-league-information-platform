import json
from re import sub
from copy import deepcopy
import csv

#ADAD STUFF
games = json.load(open('out_2.json'))

def solr(game):
    del game['home_team']['lineup']
    del game['home_team']['subs']
    del game['away_team']['lineup']
    del game['away_team']['subs']
    for player in game['home_team']['squad']:
        player['events'] = []
        for key in ['goals', 'own_goals', 'yellows', 'reds', 'sub_on', 'sub_off', 'missed_pens']:
            player['events'].append({'name': key, 'count': player[key]})
            del player[key]
    
    for player in game['away_team']['squad']:
        player['events'] = []
        for key in ['goals', 'own_goals', 'yellows', 'reds', 'sub_on', 'sub_off', 'missed_pens']:
            player['events'].append({'name': key, 'count': player[key]})
            del player[key]

    return game


json.dump(list(map(solr, games)), open('out_3.json', 'w'), ensure_ascii=False)

#######################################3

# def remove_readmore(game):
#     game['report'] = sub(r'^.{,100}?Read more', '', game['report'])
#     game['report'] = sub(r'(?<=\.|\?).{,100}?Read more', '', game['report'])

#     return game

# games = json.load(open('games.json'))
# f = list(map(remove_readmore, games))

# json.dump(f, open('test.json', 'w'), ensure_ascii=False)