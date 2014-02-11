import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from config import configuration as cfg
from playerinfo import playerinfo
from bson.son import SON
from scoreconfig import scoreconfiguration as sconfig
sconfig = sconfig['scorearray']

client = MongoClient(cfg['deployurl'])
db = client[cfg['deploydatabase']]
cUsers = db.users
cPlayers = db.Players
cGames = db.Games



"""
Uses mongoDB aggregation pipeline to aggregate scores and sum them.
"""
def calctotalscore(player, score):
    playername = player['playername']
    return cGames.aggregate([
                {
                '$match': {'playerlist': player['playername']}
                },
                {
                '$project': {
                            score + 'score': '$players.' + playername + '.score.' + score
                            }
                },
                {
                '$group': {
                            '_id':playername,
                            'total' + score: {'$sum':'$' + score + 'score'}
                            }
                }
        ])

def calcalltotalplayerscore():
    playersquery = cPlayers.find()
    for player in playersquery:
        totalscore={}
        for score in sconfig:
            totalscore[score + 'score'] = calctotalscore(player, score + 'score')['result'][0]['total' + score + 'score']
        totalscore['totalscore'] = sum(totalscore.values())
        # pprint(totalscore)

        cPlayers.update({'playername':player['playername']}, {'$set':{'scores':totalscore}})

    


# for player in cPlayers.find({'playername':'Bjergsen'}):
#     pprint(calctotalscore(player, 'kdascore'))

calcalltotalplayerscore()

# for user in cUsers.find():
#     print(user)
#     if 'rosterarray' not in user:
#         print('lol not found')
#     else:
#         roster1 = cPlayers.aggregate([
#                 {
#                 '$match': {'playername':{'$in':user['rosterarray']}}
#                 }
#             ])['result']

#         roster = {}
#         for player in roster1:
#             roster[player['role']] = player['_id']
#         print(roster)
#         cUsers.update({'username':user['username']}, {'$set':{'roster':roster}})

