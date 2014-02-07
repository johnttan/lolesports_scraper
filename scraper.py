from pyquery import PyQuery as pq
import json
from pprint import pprint
from config import configuration as cfg
from playerinfo import playerinfo as playerinfo

"""
This function processes the dictionary of match data
by adding, removing and modifying various keys and values.
"""
def processGame(jsonmatchdata):
    matchnumber = list(jsonmatchdata)[0]
    matchdoc = jsonmatchdata[matchnumber]

    if cfg['dev']:
        print('gameID: ' + str(matchnumber))
    if int(matchnumber) in cfg['gamematchnumbers']['na']:
            region = 'na'
    elif int(matchnumber) in cfg['gamematchnumbers']['eu']:
            region = 'eu'
    elif int(matchnumber) == 2156:
            matchnumber = 1883
            region = 'na'
    else:
        return 'Error: Match number not recognized'

    winteamname = ''
    winteamid = ''
    loseteamname = ''
    loseteamid = ''
    for teamid, team in matchdoc.items():
        for playerid, player in team.items():
            """rename some key fields and store match information. region, matchid, etc."""
            player['playername'] = player.pop('player field')
            player['teamid'] = teamid
            player['matchid'] = matchnumber
            player['region'] = region
            player['playerid'] = playerid
            player['teamid'] = teamid
            player['teamname'] = playerinfo[player['playername']][1]
            player['role'] = playerinfo[player['playername']][0]

            """determine which team won and which team lost. store that info."""
            if player['win'] == 1:
                winteamname = player['teamname']
                winteamid = teamid
            elif player['win'] == 0:
                loseteamname = player['teamname']
                loseteamid = teamid
                
        """switch key names to 'winteam' and 'loseteam'. assign appropriate team."""
        for playerid, player in team.items():
            playername = player['playername']
            team[playername] = team.pop(playerid)

    matchdoc['winteamname'] = winteamname
    matchdoc['winteamid'] = winteamid
    matchdoc['loseteamname'] = loseteamname
    matchdoc['loseteamid'] = loseteamid

    matchdoc['winteam'] = matchdoc.pop(matchdoc['winteamid'])
    matchdoc['loseteam'] = matchdoc.pop(matchdoc['loseteamid'])

    matchdoc['gameID'] = matchnumber
    matchdoc['region'] = region
    return matchdoc

def retrieveGame(url):
    page = pq(url=url)
    if cfg['dev']['log']:
        print(url)
    parsedpage = page("script:contains('jQuery.extend')").html()[31:-2]
    jsonmatchdata = json.loads(parsedpage)["esportsDataDump"]["matchDataDump"]
    return jsonmatchdata

"""
Runs necessary functions to retrieve, parse, and format the match data.
Returns a dictionary with match data.
"""
def retrieveandprocessGame(urlmatchnumber):
    if cfg['dev']['log']:
        print('URLmatch: ' + str(urlmatchnumber))
    url = cfg['retrieveurl'] + str(urlmatchnumber)
    jsonmatchdata = retrieveGame(url)
    matchdoc = processGame(jsonmatchdata)
    
    matchdoc['URLmatchnumber'] = urlmatchnumber
    return matchdoc

"""
Tests
"""
def _testNA():
        for urlmatchnumber in cfg['urlmatchnumbers']['na']:
            retrieveandprocessGame(urlmatchnumber)
def _testEU():
        for urlmatchnumber in cfg['urlmatchnumbers']['eu']:
            retrieveandprocessGame(urlmatchnumber)

if cfg['dev']['scraper']:
    try:
        _testNA()
    except KeyError:
        print('No more games NA')

    try:
        _testEU()
    except KeyError:
        print('No more games EU')

#For singular test cases. Accepts urlmatchnumber as argument. Refer to config.py
# pprint(retrieveandprocessGame(1693))
