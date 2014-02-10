import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from config import configuration as cfg
from playerinfo import playerinfo

client = MongoClient(cfg['deployurl'])
db = client[cfg['deploydatabase']]
cUsers = db.Users
cPlayers = db.Players
cGames = db.Games
cPlayers.create_index("playername", unique=True)
def initializeplayers():
    for playername, info in playerinfo.items():
        player = {
        'playername': playername,
        'teamname': info[1],
        'role': info[0],
        'statistics': {},
        'latestgame': {},
        'gamesplayed': []
        }
        cPlayers.update({'playername':playername}, player, upsert=True)

def updateplayerdata():
    for playername, info in playerinfo.items():
        gamesplayed = []
        gamesplayedarray = []
        latestgameplayedid = 0
        gamesplayedquery = cGames.find({'playerlist': playername},)
        for game in gamesplayedquery:
            gamesplayed.append(game)
        for game in gamesplayed:
            gamesplayedarray.append(game['gameID'])
        for game in gamesplayed:
            if game['gameID'] == max(gamesplayedarray):
                latestgame = game

        cPlayers.update({'playername':playername}, {'$set':{'gamesplayed':gamesplayed, 'latestgame':latestgame}})

def updateplayerdatabygame(game):
    for playername, player in game['players'].items():
        for player in cPlayers.find({'playername':playername}):
            if not any(game1['gameID'] == game['gameID'] for game1 in player[gamesplayed]):
                cPlayers.update({'playername':playername}, {'$set':{'gamesplayed':gamesplayed}})


if cfg['dev']['playerdatabase']:
    initializeplayers()
    updateplayerdata()
