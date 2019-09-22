import bs4, requests, html
import re
import datetime as dt
from bs4.dammit import EncodingDetector
from newspaper import Article

def getSoup(matchUrl):
    res = requests.get(matchUrl)
    res.raise_for_status()

    http_encoding = res.encoding if 'charset' in res.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(res.content, is_html=True)
    encoding = html_encoding or http_encoding

    return bs4.BeautifulSoup(res.content, 'lxml', from_encoding=encoding)
    #return bs4.BeautifulSoup(res.text, 'lxml')

def getTeam(team, matchSoup):
    lineup = []
    subs = []
    CUTOFF = 11 #11 starters
    team_div = matchSoup.select('div.team-lineups__list-team')[team]

    #TODO: Not store red cards and subs as lists? They are a at most once type of event

    for starter in team_div.select('ul.team-lineups__list-group > li')[:CUTOFF]:
        current_player = {}
        current_player['name'] = starter.select_one('span.team-lineups__list-player-name').text.replace('(c)', '').strip()
        event_list = starter.select('span.team-lineups__list-events > span')
        current_player['yellows'] = [event.text.strip() for event in event_list if 'yellow_card' in event.select_one('img')['src']]
        current_player['reds'] = [event.text.strip() for event in event_list if 'red_card' in event.select_one('img')['src']]
        current_player['own_goals'] = [event.text.strip() for event in event_list if 'own_goal' in event.select_one('img')['src']]
        current_player['goals'] = [event.text.strip() for event in event_list if 'goal' in event.select_one('img')['src'] or 'penalty' in event.select_one('img')['src'] and 'own_goal' not in event.select_one('img')['src']]
        current_player['sub_off'] = [event.text.strip() for event in event_list if 'substitution_off' in event.select_one('img')['src']] 
        lineup.append(current_player)
    
    for sub in team_div.select('ul.team-lineups__list-group > li')[CUTOFF:]:
        current_player = {}
        current_player['name'] = sub.select_one('span.team-lineups__list-player-name').text.replace('(c)', '').strip()
        event_list = sub.select('span.team-lineups__list-events > span')
        current_player['yellows'] = [event.text.strip() for event in event_list if 'yellow_card' in event.select_one('img')['src']]
        current_player['reds'] = [event.text.strip() for event in event_list if 'red_card' in event.select_one('img')['src']]
        current_player['own_goals'] = [event.text.strip() for event in event_list if 'own_goal' in event.select_one('img')['src']]
        current_player['goals'] = [event.text.strip() for event in event_list if 'goal' in event.select_one('img')['src'] or 'penalty' in event.select_one('img')['src'] and 'own_goal' not in event.select_one('img')['src']]
        current_player['sub_on'] = [event.text.strip() for event in event_list if 'substitution_on' in event.select_one('img')['src']]
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

    for fixture in seasonSoup.select('div.fixres__item')[4:5]: #TODO: Remove hardcoded cut
        print("URL: %s" % fixture.find('a')['href'])
        print("Home Team: {} {}".format(fixture.select_one('span.matches__participant--side1 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[0].text.strip()))
        print("Away Team: {} {}".format(fixture.select_one('span.matches__participant--side2 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[1].text.strip()))
        
        urlSplited = fixture.find('a')['href'].rsplit('/', 1)
        lineupUrl = '%s/teams/%s' % (urlSplited[0], urlSplited[1])
        matchSoup = getSoup(lineupUrl)

        #3 items on details: Matchup, match date and arena+attendance
        match_details = matchSoup.select('li.match-header__detail-item')
        #extract matching capturing groups (full match, day of month, month in full name)
        match_re_match = re.search('(?:\d{1,2}\:\d{2}\s(?:am|pm)\s)?(?:[a-zA-Z]+?\s)(\d{1,2})(?:st|nd|rd|th)\s(\w+)', match_details[1].text).groups()
        #create timestamp from matched information
        match_date = dt.datetime.strptime('%s %s %d' % (*match_re_match, seasonYear if match_re_match[1] not in ['September, October, November, December'] else seasonYear-1), '%d %B %y')
        #print(match_date.strftime('%d/%m/%Y'))

        home = getTeam(0, matchSoup)
        away = getTeam(1, matchSoup)
        print("Home lineup: %s" % home[0])
        print()
        print("Away lineup: %s" % away[0])
        print()
        print("Home subs: %s" % home[1])
        print()
        print("Away subs: %s" % away[1])

        reportUrl = '%s/report/%s' % (urlSplited[0], urlSplited[1])
        article = Article(reportUrl)
        article.download()
        article.parse()
        print("Match report: %s" % article.text)

        

getSeason(19)


# https://www.skysports.com/premier-league-results/2018-19

# https://github.com/codelucas/newspaper

# from newspaper import Article
# url = 'https://www.skysports.com/football/hull-city-vs-leicester/report/356341'
# article = Article(url)
# article.download()
# article.parse()
# article.text

# matchSoup = getSoup('https://www.skysports.com/football/tottenham-vs-brighton/teams/391084')
# teamHome = getTeamLineup(1, matchSoup)
# print('')
# teamAway = getTeamLineup(2, matchSoup)

# print('')
# matchSoup = getSoup('https://www.skysports.com/football/arsenal-vs-fulham/teams/210836')
# teamHome = getTeamLineup(1, matchSoup)
# print('')
# teamAway = getTeamLineup(2, matchSoup)
