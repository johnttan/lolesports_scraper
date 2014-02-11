import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from config import configuration as cfg
from playerinfo import playerinfo
from bson.son import SON
from scoreconfig import scoreconfiguration as sconfig

client = MongoClient(cfg['deployurl'])
db = client[cfg['deploydatabase']]
cUsers = db.users
cPlayers = db.Players
cGames = db.Games

def updateranks():
    playerranks = cPlayers.aggregate([
        {
            '$match':{}
        },
        {
            '$sort': {'scores.totalscore': -1}
        },
        {
            '$project':{'playername': 1, 'scores.totalscore': 1}
        }

        ])['result']

    print(playerranks)