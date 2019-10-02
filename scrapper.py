import bs4, requests, html
import re
import datetime as dt
from bs4.dammit import EncodingDetector
from newspaper import Article
from timeit import default_timer as timer
import json
import os

def getSoup(matchUrl):
    res = requests.get(matchUrl)
    res.raise_for_status()

    http_encoding = res.encoding if 'charset' in res.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(res.content, is_html=True)
    encoding = html_encoding or http_encoding

    return bs4.BeautifulSoup(res.content, 'lxml', from_encoding=encoding)

def getTeam(team, matchSoup):
    lineup = []
    subs = []
    CUTOFF = 11 #11 starters
    team_div = matchSoup.select('div.team-lineups__list-team')[team]

    for starter in team_div.select('ul.team-lineups__list-group > li')[:CUTOFF]:
        current_player = dict()
        current_player['name'] = starter.select_one('span.team-lineups__list-player-name').text.replace('(c)', '').strip()
        event_list = starter.select('span.team-lineups__list-events > span')
        current_player['yellows'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'yellow_card' in event.select_one('img')['src']]
        current_player['reds'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'red_card' in event.select_one('img')['src']]
        current_player['own_goals'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'own_goal' in event.select_one('img')['src']]
        current_player['goals'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if re.search('((?<!own_)goal)|penalty(?!_missed)', event.select_one('img')['src']) is not None]
        current_player['missed_pens'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'penalty_missed' in event.select_one('img')['src']]
        current_player['sub_off'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'substitution_off' in event.select_one('img')['src']] 
        lineup.append(current_player)
    
    for sub in team_div.select('ul.team-lineups__list-group > li')[CUTOFF:]:
        current_player = dict()
        current_player['name'] = sub.select_one('span.team-lineups__list-player-name').text.replace('(c)', '').strip()
        event_list = sub.select('span.team-lineups__list-events > span')
        current_player['yellows'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'yellow_card' in event.select_one('img')['src']]
        current_player['reds'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'red_card' in event.select_one('img')['src']]
        current_player['own_goals'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'own_goal' in event.select_one('img')['src']]
        current_player['goals'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if re.search('((?<!own_)goal)|penalty(?!_missed)', event.select_one('img')['src']) is not None]
        current_player['missed_pens'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'penalty_missed' in event.select_one('img')['src']]
        current_player['sub_on'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'substitution_on' in event.select_one('img')['src']]
        current_player['sub_off'] = [int(re.sub(r'(\+\d+)?\'','',event.text.strip())) for event in event_list if 'substitution_off' in event.select_one('img')['src']]
        subs.append(current_player)
    
    return (lineup, subs)

def getSeason(seasonYear):
    seasonUrl = 'https://www.skysports.com/premier-league-results/20%02d-%02d' % (seasonYear - 1, seasonYear)
    seasonSoup = getSoup(seasonUrl)

    # Make sure page renders all matches beforehand (no "Show more...")
    # Just trust that this works
    script_tag = seasonSoup.select_one('script[type="text/show-more"]')
    hidden_fixtures = script_tag.text
    script_tag.insert_before(bs4.BeautifulSoup(hidden_fixtures, 'html.parser'))
    script_tag.decompose()
    seasonSoup = bs4.BeautifulSoup(seasonSoup.renderContents(), 'html.parser')

    games = []

    filename = '{}-{}.json'.format(seasonYear-1, seasonYear)
    exists = os.path.exists(filename)
    f = open(filename, 'a' if exists else 'w')
    if not exists:
        f.write('[')
    # Process games
    start = 300
    end = 380
    for fixture in seasonSoup.select('div.fixres__item')[start:end]:
        game = dict()
        #Get team names and scores
        #print("URL: %s" % fixture.find('a')['href'])
        #print("Home Team: {} {}".format(fixture.select_one('span.matches__participant--side1 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[0].text.strip()))
        #print("Away Team: {} {}".format(fixture.select_one('span.matches__participant--side2 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[1].text.strip()))
        home_team = fixture.select_one('span.matches__participant--side1 span.swap-text__target').text
        #home_score = int(fixture.select('span.matches__teamscores-side')[0].text.strip())
        away_team = fixture.select_one('span.matches__participant--side2 span.swap-text__target').text
        #away_score = int(fixture.select('span.matches__teamscores-side')[1].text.strip())

        #Deconstruct URL so as to easily construct lineups and report URL from it later
        urlSplited = fixture.find('a')['href'].rsplit('/', 1)

        #Get match soup
        lineupUrl = '%s/teams/%s' % (urlSplited[0], urlSplited[1])
        matchSoup = getSoup(lineupUrl)

        #Get match details (date, arena, attendance)
        match_details = matchSoup.select('li.match-header__detail-item')

        #Get date
        #Extract matching capturing groups (full match, day of month, month in full name)
        match_date_groups = re.search('(?:\d{1,2}\:\d{2}\s(?:am|pm)\s)?(?:[a-zA-Z]+?\s)(\d{1,2})(?:st|nd|rd|th)\s(\w+)', match_details[1].text).groups()
        #create timestamp from matched information
        match_date = dt.datetime.strptime('%s %s %d' % (*match_date_groups, seasonYear if match_date_groups[1] not in ['September, October, November, December'] else seasonYear-1), '%d %B %y').strftime('%d/%m/%Y')

        #Get arena and attendance
        match_arena_groups = re.search('([\w\s,\'\-]+\w+)\s+(?:\(Att:\s(\d+)\))?', match_details[2].text).groups()
        match_arena = match_arena_groups[0]
        match_attendance = int(match_arena_groups[1] if match_arena_groups[1] is not None else 54986) #TODO: Obviously remove this later...

        game['date'] = match_date
        game['arena'] = match_arena
        game['attendance'] = match_attendance
        

        home_players = getTeam(0, matchSoup)
        away_players = getTeam(1, matchSoup)
        # print("Home lineup: %s" % home_players[0])
        # print()
        # print("Away lineup: %s" % away_players[0])
        # print()
        # print("Home subs: %s" % home_players[1])
        # print()
        # print("Away subs: %s" % away_players[1])

        game['home_team'] = dict()
        game['home_team']['name'] = home_team
        game['home_team']['lineup'] = home_players[0]
        game['home_team']['subs'] = home_players[1]

        game['away_team'] = dict()
        game['away_team']['name'] = away_team
        game['away_team']['lineup'] = away_players[0]
        game['away_team']['subs'] = away_players[1]

        reportUrl = '%s/report/%s' % (urlSplited[0], urlSplited[1])
        article = Article(reportUrl, language='en')
        article.download()
        article.parse()
        match_report = article.text

        game['report'] = re.sub(r'\n+', r' ', match_report) #Replace unwanted new lines with whitespaces
        # print("Match report: %s" % article.text)

        #games.append(game)
        json.dump(game, f, ensure_ascii=False)
        f.write(',')
        #print("Game processed")
    
    
    f.close()
    return games

        
if __name__ == '__main__':
    t = -timer()
    season = 16
    games = getSeason(season)
    t = t + timer()
    print("Time: %s" % str(t))
    print("Done")
    
