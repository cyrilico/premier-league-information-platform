import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from functools import reduce

sns.set_palette("dark")

games = []
for key in ['14-15','15-16','16-17','17-18','18-19']:
    games.extend(json.load(open('{}.json'.format(key))))

goals = dict()
cards = dict()
subs = dict()

for game in games:
    for starter_home in game['home_team']['lineup']:
        for goal_1 in starter_home['goals']+starter_home['own_goals']:
            goals[goal_1] = goals.get(goal_1,0)+1
        for card in starter_home['yellows']+starter_home['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in starter_home and len(starter_home['sub_on']) > 0:
            sub_min = starter_home['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1
    for sub in game['home_team']['subs']:
        for goal_2 in sub['goals']+sub['own_goals']:
            goals[goal_2] = goals[goal_2] + 1 if goal_2 in goals else 1
        for card in sub['yellows']+sub['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in sub and len(sub['sub_on']) > 0:
            sub_min = sub['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1
    for starter_away in game['away_team']['lineup']:
        for goal_3 in starter_away['goals']+starter_away['own_goals']:
            goals[goal_3] = goals[goal_3] + 1 if goal_3 in goals else 1
        for card in starter_away['yellows']+starter_away['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in starter_away and len(starter_away['sub_on']) > 0:
            sub_min = starter_away['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1
    for sub_away in game['away_team']['subs']:
        for goal_4 in sub_away['goals']+sub_away['own_goals']:
            goals[goal_4] = goals[goal_4] + 1 if goal_4 in goals else 1
        for card in sub_away['yellows']+sub_away['reds']:
            cards[card] = cards[card] + 1 if card in cards else 1
        if 'sub_on' in sub_away and len(sub_away['sub_on']) > 0:
            sub_min = sub_away['sub_on'][0]
            subs[sub_min] = subs[sub_min] + 1 if sub_min in subs else 1

card_df = pd.DataFrame([{'minute': k, 'card_count': v} for k,v in cards.items()])
sub_df = pd.DataFrame([{'minute': k, 'sub_count': v} for k,v in subs.items()])
goal_df = pd.DataFrame([{'minute': k, 'goal_count': v} for k,v in goals.items()])

final_df = card_df.merge(sub_df, how='outer', on='minute').merge(goal_df, how='outer', on='minute')

final_df = final_df.set_index('minute')
final_df = final_df.sort_index()
final_df = final_df.transpose()
final_df.T.plot()

# plt.plot( 'minute', 'card_count', data=cards, marker='', color='skyblue', linewidth=2)
# #plt.plot( 'minute', 'sub_count', data=sub_df, marker='', color='olive', linewidth=2)
# #plt.plot( 'minute', 'goal_count', data=goal_df, marker='', color='olive', linewidth=2, linestyle='dashed')
# plt.legend()
plt.show()