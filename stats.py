import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from functools import reduce

games = []
for key in ['14-15','15-16','16-17','17-18','18-19']:
    games.extend(json.load(open('{}.json'.format(key))))

print(len(games))
goals = dict()
cards = dict()
subs = dict()

for game in games:
    for starter in game['home_team']['lineup']:
        for goal in starter['goals']+starter['own_goals']:
            goals[goal] = goals[goal] + 1 if goal in goals else 1
        for card in starter['yellows']+starter['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in starter:
            sub_min = starter['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1
    for sub in game['home_team']['subs']:
        for goal in sub['goals']+starter['own_goals']:
            goals[goal] = goals[goal] + 1 if goal in goals else 1
        for card in starter['yellows']+starter['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in starter:
            sub_min = starter['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1
    for starter in game['away_team']['lineup']:
        for goal in starter['goals']+starter['own_goals']:
            goals[goal] = goals[goal] + 1 if goal in goals else 1
        for card in starter['yellows']+starter['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in starter:
            sub_min = starter['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1
    for sub in game['away_team']['subs']:
        for goal in starter['goals']+starter['own_goals']:
            goals[goal] = goals[goal] + 1 if goal in goals else 1
        for card in starter['yellows']+starter['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in starter:
            sub_min = starter['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1

print(sum(cards.values()))

