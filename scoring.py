from scoreformula import scoreformuladict as calculate
from scoreconfig import scoreconfiguration as sconfig
from pprint import pprint

def calctotalscore(score):
    return (sum(score.values()))

def calcdeathscore(playername, game, player):
    return calculate['deathscore'](player['deaths'])

def calcwinscore(playername, game, player):
    return calculate['winscore'](player['win'])

def calccsscore(playername, game, player):
    cs = player['minion_kills']
    for playername1, player1 in game['players'].items():
        if playername1 != playername and player1['role'] == player['role']:
            oppcs = player1['minion_kills']
    role = player['role']
    csscore = calculate['csscore'](cs, oppcs, role)
    return csscore

def calcgoldscore(playername, game, player):
    gold = player['total_gold']
    gamegold = 0
    for playername1, player1 in game['players'].items():
        gamegold += player1['total_gold']
        if player1['teamname'] == player['teamname'] and player1['role'] == player['role']:
            oppgold = player1['total_gold']
    goldscore = calculate['goldscore'](gold, oppgold, gamegold)
    return goldscore

def calcpartscore(playername, game, player):
    kills = player['kills']
    assists = player['assists']
    teamkills = 0
    for playername1, player1 in game['players'].items():
        if player1['teamname'] == player['teamname']:
            teamkills += player1['kills']
    partscore = calculate['partscore'](kills, assists, teamkills)
    return partscore

def calckdascore(playername, game, player):
    kills = player['kills']
    deaths = player['deaths']
    assists = player['assists']
    role = player['role']
    kdascore = calculate['kdascore'](kills, deaths, assists, role)
    return kdascore


"""
Takes in game dictionary, playername
returns score dictionary for particular player
"""
def calcplayerscore(playername, game, player):
    score = {}
    for scorefield in sconfig['scorearray']:
        score[scorefield + 'score'] = globals()['calc' + scorefield + 'score'](playername, game, player)
    score['totalscore'] = calctotalscore(score)
    return score

"""
Takes in game dictionary,
returns game dictionary with all scores calculated.
This is imported in databasescoring.py
"""

def calcgamescore(game):
    for playername, player in game['players'].items():
        player['score'] = calcplayerscore(playername, game, player)

    return game


exports = {
    'calcgamescore': calcgamescore
}