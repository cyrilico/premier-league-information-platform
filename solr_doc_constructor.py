import json
from re import sub


games = []
for key in ['14-15','15-16','16-17','17-18','18-19']:
    games.extend(json.load(open('{}-fixed.json'.format(key))))

def solr(game):
    result = {}
    result['date'] = game['date']
    result['arena'] = game['arena']
    result['home_team'] = game['home_team']['name']
    result['away_team'] = game['away_team']['name']
    result['home_lineup'] = list(map(lambda p: p['name'], game['home_team']['lineup']))
    result['away_lineup'] = list(map(lambda p: p['name'], game['away_team']['lineup']))
    result['home_subs'] = list(map(lambda p: p['name'], game['home_team']['subs']))
    result['away_subs'] = list(map(lambda p: p['name'], game['away_team']['subs']))
    result['home_scorers'] = list(map(lambda p: p['name'], filter(lambda x: len(x['goals']+x['own_goals']) > 0, game['home_team']['lineup']+game['home_team']['subs'])))
    result['away_scorers'] = list(map(lambda p: p['name'], filter(lambda x: len(x['goals']+x['own_goals']) > 0, game['away_team']['lineup']+game['away_team']['subs'])))
    result['report'] = sub(r'\n+', ' ', game['report'])   
    return result


json.dump(list(map(solr, games)), open('games.json', 'w'), ensure_ascii=False)