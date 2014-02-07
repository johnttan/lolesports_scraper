import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from config import configuration as cfg
from playerinfo import playerinfo

client = MongoClient(cfg['url'], cfg['port'])
db = client[cfg['database']]
cUsers = db.Users
cPlayers = db.Players
cGames = db.Games

def initializeplayers():
    for playername, info in playerinfo.items():
        player = {
        'playername': playername,
        'teamname': info[1],
        'role': info[0],
        'statistics': {},
        'latestgame': {},
        'totalscores': {}
        }


        cPlayers.update({'playername':playername}, player, )