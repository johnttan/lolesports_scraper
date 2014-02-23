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

def calcuserscore(singleuser = None):
    if singleuser == None:
        for user in cUsers.find():
            if 'oldroster' not in user.keys():
                cUsers.update({'_id':user['_id']}, {'$set':{'oldroster':[], 'oldplayerslastgame':{}, 'newplayersfirstgame': {}}})
        users = cUsers.find()
    else:
        users = cUsers.find({'username':singleuser})
    for user in users:
        # pprint(user)
        totaluserscore = 0
        for playerrole, playerid in user['roster'].items():
            user['roster'][playerrole] = cPlayers.find_one(playerid)
        for playerrole, player in user['roster'].items():
            playername = player['playername']
            if playername in user['newplayersfirstgame'].keys():
                for game in player['gamesplayed']:
                    if game['gameID'] >= user['newplayersfirstgame'][playername]:
                        totaluserscore += game['players'][playername]['score']['totalscore']
            # elif player['playername'] in user['oldplayerslastgame'].keys():
            #     for game in player['gamesplayed']:
            #         if game['gameID'] <= user['oldplayerslastgame'][player['playername']]:
            #             totaluserscore += game['players'][player['playername']]['score']['totalscore']
            else:
                for game in player['gamesplayed']:
                    totaluserscore += game['players'][playername]['score']['totalscore']
        for player in user['oldroster']:
            if player is not None:
                for game in player['gamesplayed']:
                    if game['gameID'] <= user['oldplayerslastgame'][player['playername']]:
                        totaluserscore += game['players'][player['playername']]['score']['totalscore']
        
        cUsers.update({'username':user['username']}, {'$set':{'totaluserscore':totaluserscore}})



nyph = cPlayers.find_one({'playername':'Nyph'})
benny = cPlayers.find_one({'playername':'Benny'})
froggen = cPlayers.find_one({'playername':'Froggen'})
shook = cPlayers.find_one({'playername':'Shook'})
wickd = cPlayers.find_one({'playername':'Wickd'})
mancloud = cPlayers.find_one({'playername':'mancloud'})
araneae = cPlayers.find_one({'playername':'Araneae'})
bloodwater = cPlayers.find_one({'playername':'BloodWater'})
cUsers.update({'username':'ostonzi'}, {'$set':{'oldplayerslastgame':{}, 'newplayersfirstgame':{}, 'oldroster':[]}})
cUsers.update({'username':'Arcwelder'}, {'$set':{'oldplayerslastgame':{'Nyph':2015}, 'newplayersfirstgame':{'VandeR':2019}, 'oldroster':[nyph]}})
cUsers.update({'username':'Antiquum'}, {'$set':{'oldplayerslastgame':{'Froggen':2018, 'Benny': 1884}, 'newplayersfirstgame':{'Overpow':2019, 'Xaxus':2019}, 'oldroster':[froggen, benny]}})
cUsers.update({'username':'im24dailey'}, {'$set':{'oldplayerslastgame':{'Wickd':2018, 'Shook': 2018}, 'newplayersfirstgame':{'Darien': 2019, 'Crumbzz': 1885}, 'oldroster':[wickd, shook]}})
cUsers.update({'username':'Mini0040'}, {'$set':{'oldplayerslastgame':{'Araneae':2018}, 'newplayersfirstgame':{'dexter':1885}, 'oldroster':[araneae]}})
cUsers.update({'username':'Eudicot'}, {'$set':{'oldplayerslastgame':{'BloodWater':1884}, 'newplayersfirstgame':{'KiWiKiD':1885}, 'oldroster':[bloodwater]}})

calcuserscore()
