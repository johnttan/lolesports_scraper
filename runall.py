from database import exports as database
from databasescoring import exports as databasescoring
from playerdatabase import exports as playerdatabase
from playeraggregations import exports as playeraggregations
from userscoreaggregations import exports as userscoreaggregations


class Loldraftscraper:
    def retrievelatest(self, region):
        if region == 'na':
            database['retrievelatest']('na')
        elif region == 'eu':
            database['retrievelatest']('eu')
        else:
            return 'invalidregion'
    def scorelatest(self):
        databasescoring['nonscoredgamescoring']()
    def allgamescore(self):
        databasescoring['allgamerescore']()
    def initializeplayers(self):
        playerdatabase['initializeplayers']()
    def updateplayerdata(self):
        playerdatabase['updateplayerdata']()
    def updateplayerdatabygame(self, game):
        playerdatabase['updateplayerdatabygame'](game)
    def allpscore(self):
        playeraggregations['calcalltotalplayerscore']()
    def pscore(self, player):
        playeraggregations['calctotalscore'](player)
    def calcuserscore(self):
        userscoreaggregations['calcuserscore']()

    def updateall(self, initialize=False):
        self.retrievelatest('na')
        self.retrievelatest('eu')
        self.scorelatest()
        if initialize == True:
            self.initializeplayers()
        self.updateplayerdata()
        self.allpscore()
        self.calcuserscore()


scraper = Loldraftscraper()

scraper.updateall()


