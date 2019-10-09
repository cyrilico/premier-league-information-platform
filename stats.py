import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import csv

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

report_length_per_season = {'14-15': [], '15-16': [], '16-17': [], '17-18': [], '18-19': []}
for key in ['14-15', '15-16', '16-17', '17-18', '18-19']:
    for season_game in json.load(open('{}.json'.format(key))):
        report_length_per_season[key].append(len(season_game['report']))

report_length_df = pd.DataFrame([{'season': k, 'report_lengths': v} for k,v in report_length_per_season.items()])

#print(report_length_df)

# Graph 1
final_df = final_df.set_index('minute')
final_df = final_df.sort_index()
final_df = final_df.transpose()
final_df.T.plot()
plt.xlabel('Minutes')
plt.ylabel('Events')
plt.title('Events by Minute')

data = pd.read_csv("gamesprocessed.csv")
goals_by_season = [{'season': key, 'nr_goals': data[idx*380:(idx+1)*380]['HomeFTScore'].sum()+data[idx*380:(idx+1)*380]['AwayFTScore'].sum()} \
                    for idx, key in enumerate(['14-15', '15-16', '16-17', '17-18', '18-19'])]

csv_as_json = csv.DictReader(open('gamesprocessed.csv'), ['Date','HomeTeam','AwayTeam','HomeFTScore','AwayFTScore','HomeHTScore','AwayHTScore','Referee'])
winning_team_goals = dict()
for game in csv_as_json:
    if game['HomeFTScore'] > game['AwayFTScore']:
        winning_team_goals[game['HomeFTScore']] = winning_team_goals.get(game['HomeFTScore'], 0) + 1
    elif game['AwayFTScore'] > game['HomeFTScore']:
        winning_team_goals[game['AwayFTScore']] = winning_team_goals.get(game['AwayFTScore'], 0) + 1

winning_team_goals_df = pd.DataFrame([{'nr_goals': k, 'count': v} for k,v in winning_team_goals.items() if k != 'HomeFTScore']) #WTF filter... but it was present idk why

#print(winning_team_goals_df)

goals_by_month_season = dict()
for idx, key in enumerate(['14-15', '15-16', '16-17', '17-18', '18-19']):
    season_df = data[idx*380:(idx+1)*380]
    season_df[["day", "mm", "year"]] = season_df["Date"].str.split("/", expand=True)
    season_df_grouped = season_df.groupby(['mm'])
    #Uncomment if graphing purely goal count
    goals_by_month_season[key] = season_df_grouped['HomeFTScore'].sum()+season_df_grouped['AwayFTScore'].sum()
    #Uncomment if graphing goal count per number of games
    goals_by_month_season[key] = (season_df_grouped['HomeFTScore'].sum()+season_df_grouped['AwayFTScore'].sum())/season_df_grouped['HomeFTScore'].count()

# Graph 2
goalsBySeason = pd.DataFrame(goals_by_season)
goalsBySeason = goalsBySeason.set_index('season')
goalsBySeason.plot.bar(legend=None)
for i, v in enumerate(goalsBySeason.get('nr_goals')):
    plt.text(i - 0.15, v + 5, str(v))
plt.xlabel('Season')
plt.ylabel('Goals')
plt.title('Goals by Season')


# Graph 3
goalsByMonthSeason = pd.DataFrame(goals_by_month_season)
goalsByMonthSeason = goalsByMonthSeason.transpose()
goalsByMonthSeason = goalsByMonthSeason[['08','09','10','11','12','01','02','03','04','05']]
goalsByMonthSeason = goalsByMonthSeason.rename(columns=lambda x: calendar.month_abbr[int(x)])

ax = goalsByMonthSeason.plot.bar(stacked=True, legend='reverse')
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=reversed(handles), labels=reversed(labels), title="Months", loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.title("Goals By Month/Season")
plt.ylabel("Goals")
plt.xlabel("Season")


# Show Graphs
#plt.show()