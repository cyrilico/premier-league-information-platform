import bs4, requests, html

def getSoup(matchUrl):
    res = requests.get(matchUrl)
    res.raise_for_status()
    return bs4.BeautifulSoup(res.text, 'lxml')

def getLineup(team, matchSoup):
    result = []
    team_div = matchSoup.select('div.team-lineups__list-team')[team]

    for starter in team_div.select('ul.team-lineups__list-group > li')[:11]: #Hardcoded cut to consider only players in starting 11 (for now)
        current_player = {}
        current_player['name'] = starter.select_one('span.team-lineups__list-player-name').text.strip()
        event_list = starter.select('span.team-lineups__list-events > span')
        #TODO: Other events...?
        current_player['cards'] = [event.text.strip() for event in event_list if 'yellow_card' in event.select_one('img')['src']]
        current_player['goals'] = [event.text.strip() for event in event_list if 'goal' in event.select_one('img')['src']]
        result.append(current_player)
    
    return result

def getSeason(seasonYear):
    seasonUrl = 'https://www.skysports.com/premier-league-results/%s' % seasonYear
    seasonSoup = getSoup(seasonUrl)

    # Make sure page renders all matches beforehand (no "Show more...")
    # Just trust that this works
    script_tag = seasonSoup.select_one('script[type="text/show-more"]')
    hidden_fixtures = script_tag.text
    script_tag.insert_before(bs4.BeautifulSoup(hidden_fixtures, 'html.parser'))
    script_tag.decompose()
    seasonSoup = bs4.BeautifulSoup(seasonSoup.renderContents(), 'html.parser')

    for fixture in seasonSoup.select('div.fixres__item')[:1]: #TODO: Remove hardcoded cut
        print("URL: %s" % fixture.find('a')['href'])
        print("Home Team: {} {}".format(fixture.select_one('span.matches__participant--side1 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[0].text.strip()))
        print("Away Team: {} {}".format(fixture.select_one('span.matches__participant--side2 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[1].text.strip()))
        
        urlSplited = fixture.find('a')['href'].rsplit('/', 1)
        lineupUrl = '%s/teams/%s' % (urlSplited[0], urlSplited[1])
        matchSoup = getSoup(lineupUrl)

        print("Home lineup: %s" % getLineup(0, matchSoup))
        print("Away lineup: %s" % getLineup(1, matchSoup))

getSeason('2009-10')


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
