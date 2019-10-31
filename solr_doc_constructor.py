import json
from re import sub
from copy import deepcopy
import csv

def merge_game(game):
    with open('gamesprocessed.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if game['date'] == row[0] and game['home'] == row[1]:
                return {'home_ft_score': row[3],\
                        'away_ft_score': row[4],\
                        'home_ht_score': row[5],\
                        'away_ht_score': row[6],\
                        'referee': row[7]}


games = []
for key in ['14-15','15-16','16-17','17-18','18-19']:
    games.extend(json.load(open('scrapped_files/{}-fixed.json'.format(key))))

def solr(game):
    result = {}
    # In case nested docs are kept
    # result['home_team']['lineup'] = list(map(lambda p: p['name'], game['home_team']['lineup']))
    # result['away_team']['lineup'] = list(map(lambda p: p['name'], game['home_team']['lineup']))
    # result['home_team']['subs'] = list(map(lambda p: p['name'], game['away_team']['lineup']))
    # result['away_team']['subs'] = list(map(lambda p: p['name'], game['away_team']['subs']))


    # Not kept
    #d,m,y = game['date'].split('/')
    #result['date'] = '{}-{}-{}'.format(y,m,d)
    result['home'] = game['home_team']['name']
    result['away'] = game['away_team']['name']
    result['arena'] = game['arena']
    result['home_lineup'] = list(map(lambda p: p['name'], game['home_team']['lineup']))
    result['away_lineup'] = list(map(lambda p: p['name'], game['away_team']['lineup']))
    result['home_subs'] = list(map(lambda p: p['name'], game['home_team']['subs']))
    result['away_subs'] = list(map(lambda p: p['name'], game['away_team']['subs']))
    result['home_scorers'] = list(map(lambda p: p['name'], filter(lambda x: len(x['goals']+x['own_goals']) > 0, game['home_team']['lineup']+game['home_team']['subs'])))
    result['away_scorers'] = list(map(lambda p: p['name'], filter(lambda x: len(x['goals']+x['own_goals']) > 0, game['away_team']['lineup']+game['away_team']['subs'])))
    result['report'] = sub(r'\n+', ' ', game['report'])


    return {**result, **merge_game(result)}


json.dump(list(map(solr, games)), open('games.json', 'w'), ensure_ascii=False)