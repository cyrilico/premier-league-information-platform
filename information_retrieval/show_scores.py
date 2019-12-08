import json
from functools import reduce

data = json.load(open('18-19.json'))

for game in data:
    all_home_goals = list(map(lambda x: x['goals'], game['home_team']['lineup'])) + list(map(lambda x: x['goals'], game['home_team']['subs'])) + list(map(lambda x: x['own_goals'], game['away_team']['subs'])) + list(map(lambda x: x['own_goals'], game['away_team']['lineup']))
    home_score = 0
    for goal_list1 in all_home_goals:
        home_score = home_score + len(goal_list1)

    all_away_goals = list(map(lambda x: x['goals'], game['away_team']['lineup'])) + list(map(lambda x: x['goals'], game['away_team']['subs'])) + list(map(lambda x: x['own_goals'], game['home_team']['subs'])) + list(map(lambda x: x['own_goals'], game['home_team']['lineup']))
    away_score = 0
    for goal_list2 in all_away_goals:
        away_score = away_score + len(goal_list2)
    print("%s %s %d - %d %s" % (game['date'], game['home_team']['name'], home_score, away_score, game['away_team']['name']))