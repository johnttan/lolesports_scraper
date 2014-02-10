from scoring import calcgamescore as gamescore
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from config import configuration as cfg

client = MongoClient(cfg['deployurl'])
db = client[cfg['deploydatabase']]
cUsers = db.Users
cPlayers = db.Players
cGames = db.Games

def allgamerescore():
    for game in cGames.find():
        newgame = gamescore(game)
        newgame['scored'] = 1
        cGames.save(newgame)

def nonscoredgamescoring():
    for game in cGames.find({'scored': 0}):
        newgame = gamescore(game)
        newgame['scored'] = 1
        cGames.save(newgame)

if cfg['dev']['databasescoring']:
    nonscoredgamescoring()