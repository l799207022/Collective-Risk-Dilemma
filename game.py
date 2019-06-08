import agent as player
import numpy as np
import pandas as pd
import math

PRISK = 0.9
BETA = 1.2  # Used in fitness (measures the intensity of selection)
R = 10
M = 10
N = 100
class Game():
    def __init__(self, nPlayer =100, mPlayer = 10, learn=True,simulation= False, prisk=PRISK, sigma=SIGMA):
        self.N = nPlayer
        self.M = mPlayer
        self.R = R
        self.learn=learn
        self.simulation = simulation
        self.prisk = 0.9
        self.fitness = [0]*self.N
        self.payoffsList = [[] for i in range (self.N)]
        self.commonPool = 0 
        self.cContributions=[0,0,0,0]
        self.iniEnvironment(self.prisk)
        self.payoffs = [[] for i in range(self.N)]
        self.proportion1 = [0.1,0.1,0.8]
        self.proportion2 = [0.1,0.8,0.1]
        self.proportion3 = [0.9,0.05,0.05]
        self.proportion4 = [0.9,0.05,0.05]
        self.proportion5 = [0.05,0.9,0.05]
        self.proportion6 = [0.05,0.9,0.05]
        # self.proportion5 = [0.1,0.8,0.1]
        # self.proportion6 = [0.05,0.9,0.05]
        self.playerAction1 = player.Agent(R,M,self.learn,self.proportion1,self.proportion2,"1")
        self.playerAction2 = player.Agent(R,M,self.learn,self.proportion3,self.proportion4,"2")
        self.playerAction3 = player.Agent(R,M,self.learn,self.proportion5,self.proportion6,"3") 
        # self.playerAction3 = player.Agent(R,M,self.learn,self.proportion5,self.proportion6,"3")
        self.playerAction =[self.playerAction1,self.playerAction2,self.playerAction3]
        self.numChange = []
        self.typeNum = [0,0,0]
        self.num1 = []
        self.num2 = []
        self.num3 = []
        self.trainTimes=0

    ## select the player from the population      
    def selectPlayers (self):
        return np.random.choice(self.N,self.M,replace=False)

    ## Update poplation in wright fisher process
    def updatePopulation(self):
        print ("fitness : ",len (self.fitness))
        prob = list(map(lambda x: x / sum(self.fitness), self.fitness))
        #print ("prob", prob)
        reproduction_selection = np.random.choice(N, N, True, prob)
        newStrategyList = [0]*N
        for i, iplayer in enumerate (reproduction_selection):
            newStrategyList[i] = self.strategyList[iplayer]
        self.strategyList = newStrategyList
        self.payoffs = [[] for i in range(N)]

    def lossfrac(self, alpha):

        """the percentage of wealth that players are going to lose if collective-risk happens"""

        for risk in range(0,1):
           return risk


    # def riskfunc(self,RF,contribution,anything):
    
    #     """the probabity of collective-risk happening, given contribution"""

    #     if RF == 1:
    #         return  # probably parse more parameters here
    #     elif RF == 2:
    #         return 1
    #     return 0

    ## Calculate the payoff
    def computePayoff(self,iplayer,invested,achieved=True):

        if self.commonPool >= R*M or np.random.random() < np.random.choice([True, False], 1, True, [1 - self.prisk, self.prisk]):
            
            return (2 * R) - invested
        else :
            return 0
    ## update the fitness
    def updateFitness (self):

        for n in range (N):
            self.fitness [n] = math.exp (BETA * np.mean(self.payoffs[n]))
    
    def getFitness (self):

        return self.fitness
    

    ## Old Train function 
    # def train(self,PRISK):
    #     # play one game with R rounds00
    #     self.prisk = PRISK 
    #     moneyGiven = [[] for i in range (M)]
    #     selectPlayers = self.selectPlayers()
    #     contribute = [0]*self.N
    #     target = self.R* self.M 
    #     # r is the roound number and R is the total round 
    #     for tPlayer in range(len(self.playerAction)):
    #         self.commonPool = 0
           
    #         # print ("the Agent:", tPlayer)
    #         # print ("otherTwo", self.playerAction[tPlayer].proportion1,self.playerAction[tPlayer].proportion2)
    #         self.playerAction[tPlayer].setLearnModel(True)
    #         for r in range(R):
    #             if self.commonPool < target:
    #                 for i , iplayer in enumerate(selectPlayers) :
    #                     # print("length of select",len(selectPlayers))
    #                     # print("player ID",i)
    #                     contribute[iplayer]=self.playerAction[tPlayer].chooseAction(self.commonPool,r,self.strategyList[iplayer])
    #                     self.commonPool += contribute[iplayer] 
    #                     # print("select plater",self.strategyList[iplayer])
    #                     if self.strategyList[iplayer] == 0 :
    #                         self.playerAction[tPlayer].envFeedback (self.commonPool,i,r,contribute[iplayer])

                           
                
    #             # elif self.commonPool >=target: 
    #             #     print ("where is this ")
    #             #     self.commonPool += self.commonPool * DELTA
    #             #     break 
    #         # print ("contribute",contribute)
    #     self.trainTimes=self.trainTimes+1
    #     print ("trainTimes:",self.trainTimes)
    #     if self.trainTimes == 50:
    #         for tPlayer in range(len(self.playerAction)):
    #             print("tplater::::::::::::::",tPlater)
    #             self.playerAction[tPlayer].updateTProprtion()
    #         self.trainTimes = 0

    ## The train function which is used for this project
    def newTrain (self,PRISK):
        priskn= PRISK
        selectPlayers=[0,1,2]
        roundc = [0,0,0]
        round = self.R
        moneyGiven = [[] for i in range(3)]
        roundTarget = 3  
        Target = 30
        for tPlayer in range(len(self.playerAction)):
            commonPool = 0
            pContribute=0
            print("**************Train player",self.playerAction[tPlayer].name,"***************")
            self.playerAction[tPlayer].setLearnModel(True)
            for r in range (R):
                if commonPool < Target:
                    roundpool = 0
                    for i in range(3):
                        # print("player",i)
                        roundc[i] = self.playerAction[tPlayer].chooseAction(self.commonPool,r,selectPlayers[i])
                        # print ("choose ", roundc[i])
                        roundpool = roundpool + roundc[i]
                        commonPool = commonPool + roundc[i]
                        if i == 0:
                            pContribute =  pContribute + roundc[0]

                    if commonPool >= (roundTarget*(r+1)):
                        # print ("total contribute", pContribute)
                        # print ("commonPool is ", commonPool)
                        # print ("choice ", roundc)
                        self.playerAction[tPlayer].newEnvFeedback(True,roundc[0],r,commonPool,pContribute)
                        
                    else:
                        self.playerAction[tPlayer].newEnvFeedback(False,roundc[0],r,commonPool,pContribute)
                        # print ("total contribute", pContribute)

        self.trainTimes=self.trainTimes+1
        print ("trainTimes:",self.trainTimes)
        if self.trainTimes == 100:
            print("updateTP####################")
            for tPlayer in range(len(self.playerAction)):
                print ("this is TP for player:",self.playerAction[tPlayer].name)
                self.playerAction[tPlayer].updateTProprtion()
            self.trainTimes = 0
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                

    ## Game play function 
    def play (self,PRISK):
        contribute = [0]*self.M
        selectPlayers = self.selectPlayers()
        target = self.R* self.M 
        self.commonPool=0
        
        for r in range(R):
                if self.commonPool < target:
                    for i , iplayer in enumerate(selectPlayers) :
                        #contribute[i]=playerAct.chooseAction(self.commonPool,r,self.strategyList[iplayer])
                        contribute[i]=self.playerAction[self.strategyList[iplayer]].chooseAction(self.commonPool,r,0)
                        self.commonPool += contribute[i] 

        for i, iplayer in enumerate(selectPlayers):
            self.payoffs[iplayer].append(self.computePayoff(iplayer, contribute[i],(self.commonPool >= target)))
        
        for i in range(M):
            if contribute[i] == 0:
                self.cContributions[0] += 1
            elif contribute[i] == R:
                self.cContributions[1] += 1
            elif contribute[i] > R:
                self.cContributions[2] += 1
            elif contribute[i] < R:
                self.cContributions[3] += 1
            else: 
                print ("Impossible")

        self.table = self.playerAction1.table
        if self.commonPool >= target :
            return 1
        else:
            return 0

    def GetcContributions(self):

        return self.cContributions
    
    def GetCommonPool(self):
        
        return self.commonPool

    def GetAverageFitness(self):

        return np.mean(self.fitness)

    def GetAveragePayoff(self):
        payoff_sum = 0
        for n in range(N):
            payoff_sum += np.mean(self.payoffs[n])
        return np.mean(payoff_sum)

    ## print the look-up table    
    def printTable (self):
        print (self.playerAction1.table,"\n")
        print (self.playerAction2.table,"\n")
        print (self.playerAction3.table,"\n")
    
    ## set the model of this game 
    def learnModel(self,learnMod = True):
        self.learn = learnMod
        print("learnModel",self.learn)
    ## ser rge model  of this game 
    def simulationModel(self,simulation =True):
        self.simulation = simulation
        print("simulaitonModel",self.simulation)
    ## set thge proportion for the environment 
    def setProportion (self,prop1,prop2):
        self.proportion1 = prop1
        self.proportion2 = prop2
    ## update the table 
    def prepareForPlay(self):
        for tPlayer in range(3):
            self.playerAction[tPlayer].updateTable()
            self.playerAction[tPlayer].setLearnModel(False)
    ## initial Environment 
    def iniEnvironment(self,risk):
        self.strategyList = np.random.choice(3,N,True,[0.333334,0.333333,0.333333])
        self.calculateType()
        self.numInitial = self.typeNum
        self.prisk =risk
        print("environment rebuilded and risk set as ",self.prisk)

    ## initial environment with diferent proportion this will be used in Wright-fisher
    def iniEnvironment1(self,risk,ratio=[0.25,0.25,0.5]):
        self.strategyList = np.random.choice(3,N,True,ratio)
        self.calculateType()
        self.numInitial = self.typeNum
        self.prisk =risk
        print("environment rebuilded and risk set as ",self.prisk)
    ## Calculate the strategy type in the population 
    def calculateType (self):
        self.typeNum=[0,0,0]
        for i in range(self.N) :
            if self.strategyList[i] == 0:
                self.typeNum [0] = self.typeNum[0] +1
            if self.strategyList[i] == 1:
                self.typeNum [1] = self.typeNum[1] +1
            if self.strategyList [i] == 2:
                self.typeNum [2] = self.typeNum[2] +1
        print ("typeNum,S1,S2,S3", self.typeNum)
        return self.typeNum
    ## Collect the change of the type Num
    def collectTypeNum (self):
        newtypeNum = self.calculateType()
        if self.numChange ==[] :
            self.numChange = [newtypeNum]
        else:
            print("numchange :", self.numChange)
            self.numChange.append(newtypeNum)
        
        self.num1.append(self.typeNum[0])
        self.num2.append(self.typeNum[1])
        self.num3.append(self.typeNum[2])
        print("numchange : : :",self.numChange)

    ## Collect the initial TypeNum
    def collectInitial (self):

        if self.simulation == True:
            numIni = self.calculateType()
            if self.numInitial ==[]:
                self.numInitial= [numIni]
            else:
                self.numInitial.append(numIni)
            
        



