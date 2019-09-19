import bs4, requests, html

def getSoup(matchUrl):
    res = requests.get(matchUrl)
    res.raise_for_status()
    return bs4.BeautifulSoup(res.text, 'lxml')

def getLineup(team, matchSoup):
    result = []
    team_div = matchSoup.select('div.team-lineups__list-team')[team]

    for starter in team_div.select('ul.team-lineups__list-group > li')[:11]: #Hardcoded cut to consider only players in starting 11 (for now)
        result.append(starter.select_one('span.team-lineups__list-player-name').text.strip())
    
    return result

    # matchYear = matchSoup.select(' h3.page-header__breadcrumb-title > a:nth-child(1)')[0].text.rsplit(' ', 1)[1]
    # print(matchYear)
    # if matchYear > '2016':
    #     teamSelector += 1

    # teamName = matchSoup.select('div.team-lineups__list-team:nth-child(%s) > div:nth-child(1) > h3:nth-child(1)'  %(teamSelector))[0].text.strip()
    # teamTactics = matchSoup.select('div.team-lineups__list-team:nth-child(%s) > div:nth-child(1) > span:nth-child(2)'  %(teamSelector))[0].text.strip()
    # print('%s - %s' %(teamName, teamTactics))
    # for playerNo in list(range(11)):
    #     playerNumber = matchSoup.select('div.team-lineups__list-team:nth-child(%s) > ul:nth-child(2) > li:nth-child(%s) > a:nth-child(1) > span:nth-child(1)' %(teamSelector, playerNo+1))[0].text.strip()
    #     playerName = matchSoup.select('div.team-lineups__list-team:nth-child(%s) > ul:nth-child(2) > li:nth-child(%s) > a:nth-child(1) > span:nth-child(2)' %(teamSelector, playerNo+1))[0].text.strip()
    #     playerEvents = matchSoup.select('div.team-lineups__list-team:nth-child(%s) > ul:nth-child(2) > li:nth-child(%s) > a:nth-child(1) > span:nth-child(3)' %(teamSelector, playerNo+1))
    #     print('%s - %s' % (playerNumber, playerName))
    #     for playerEvent in playerEvents[0].select('span'):
    #         eventType = playerEvent.select('img')[0]['src'].rsplit('/', 1)[-1]
    #         eventTime = playerEvent.text.strip()
    #         print('    %s - %s' %(eventType, eventTime))
    # return ''

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

    for fixture in seasonSoup.select('div.fixres__item')[:1]:
        print("URL: %s" % fixture.find('a')['href'])
        print("Home Team: {} {}".format(fixture.select_one('span.matches__participant--side1 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[0].text.strip()))
        print("Away Team: {} {}".format(fixture.select_one('span.matches__participant--side2 span.swap-text__target').text, fixture.select('span.matches__teamscores-side')[1].text.strip()))
        
        urlSplited = fixture.find('a')['href'].rsplit('/', 1)
        lineupUrl = '%s/teams/%s' % (urlSplited[0], urlSplited[1])
        matchSoup = getSoup(lineupUrl)

        print("Home lineup: %s" % getLineup(0, matchSoup))
        print("Away lineup: %s" % getLineup(1, matchSoup))


    # for i in range(2, 20):
    #     testDate = seasonSoup.select('div.fixres__item:nth-child(%s)' % i)
        
    #     if(len(testDate) == 0):
    #         gameDate = seasonSoup.select('h4.fixres__header2:nth-child(%s)' % i)[0].text.strip()
    #         print(gameDate)
    #     else:      
    #         game = seasonSoup.select('div.fixres__item:nth-child(%s) > a:nth-child(1)' % i)
    #         gameUrl = game[0]['href']
    #         homeTeam = seasonSoup.select('div.fixres__item:nth-child(%s) > a:nth-child(1) > span:nth-child(2) > span:nth-child(1) > span:nth-child(1)' % i)[0].text.strip()
    #         homeScore = seasonSoup.select('div.fixres__item:nth-child(%s) > a:nth-child(1) > span:nth-child(3) > span:nth-child(1) > span:nth-child(1)' % i)[0].text.strip()
    #         awayScore = seasonSoup.select('div.fixres__item:nth-child(%s) > a:nth-child(1) > span:nth-child(3) > span:nth-child(1) > span:nth-child(2)' % i)[0].text.strip()
    #         awayTeam = seasonSoup.select('div.fixres__item:nth-child(%s) > a:nth-child(1) > span:nth-child(4) > span:nth-child(1) > span:nth-child(1)' % i)[0].text.strip()
    #         print('%s - %s - %s - %s - %s' %(gameUrl, homeTeam,homeScore, awayScore, awayTeam))
    #         urlSplited = gameUrl.rsplit('/', 1)
    #         lineupUrl = '%s/teams/%s' % (urlSplited[0], urlSplited[1])
    #         matchSoup = getSoup(lineupUrl)
    #         getTeamLineup(1, matchSoup)
    #         getTeamLineup(2, matchSoup)
    #         print(' ')
    # return ''

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
