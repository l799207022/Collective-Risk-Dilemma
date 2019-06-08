
import numpy as np 
import pandas as pd 

PsyPoint = 1.2
BETA = 1.2
class Agent():
   
    def __init__(self,roundNum=10, mplayers =10,learn =True,prop1=[0.4,0.4,0.2],prop2=[0.6,0.3,0.1],name="1"):

        'add variables to construct agent instance and define instance variables'
        self.name = name 
        self.rNum = roundNum
        self.gamePayoff = []
        self.moneyOwns = 2*roundNum
        self.target = roundNum * mplayers
       # self.contribution = []
        self.action = [0,1,2]
        self.numPlayer = mplayers
        self.buildQtable()
        self.learn = learn
        self.proportion1 = prop1
        self.proportion2 = prop2
        print (self.name)
        print ("prop1",self.proportion1)
        print ("prop1",self.proportion2)
        self.feedbackTable=[]
        self.buildFeedBackTable()
        self.contribution=[]
        self.selImprove = 0
        # self.tc0 = 0.3333
        # self.tc1 = 0.3334
        # self.tc2 = 0.3333
        self.tproprtion = [[0.333,0.334,0.333] for i in range (self.rNum)]
        # self.roundMaxPoint = [0]*roundNum
        # self.maxPointChoice = []
        
    def collectPayoff (self,payoff):
        
        self.gamePayoff.append(payoff)

    ## An action choose function to select the action depend on different model and different strategy Type
    def chooseAction(self,commonPool,state,stragyType=0):
        moneyGiven=0
        strww=stragyType
        # print ("type",strww)
        # print ("learnmod",self.learn)
        if (commonPool < self.target) & (self.moneyOwns > 1):
            if (self.learn == False):
                moneyGiven = self.qChooseQAction(state)
                # moneyGiven =  np.random.choice([0,1,2],1,self.tproprtion)[0]
                self.contribution.append(moneyGiven)
                # print ("this player",self.name,"give:",moneyGiven)

                #self.contribution.append(moneyGiven)
            if (self.learn ==True):
                if stragyType == 0:
                        moneyGiven = np.random.choice([0,1,2],1,self.tproprtion[state])[0]
                        # print ("&&&&&&&",moneyGiven)
                    # self.contribution.append(moneyGiven)
                    # self.selImprove =self.selImprove +1
                    # if self.Improve 
                elif stragyType == 1:
                        moneyGiven = np.random.choice([0,1,2],1,False,self.proportion1 )[0]
                        # print ("11111111",moneyGiven)
                        #self.contribution.append(moneyGiven)
                elif stragyType == 2:
                        moneyGiven = np.random.choice([0,1,2],1,False,self.proportion2)[0]
                        # print ("2222222222222222",moneyGiven)
                else : 
                    print ("wrong choice")
        if (commonPool < self.target) & (self.moneyOwns == 1 ):
            if (stragyType == 0) | (stragyType == 1):
                moneyGiven = 1
            elif (stragyType == 2):
                moneyGiven = 0
        if (commonPool >= self.target) | (self.moneyOwns == 0):
            moneyGiven = 0
        return moneyGiven
    
    # environment feedback 
    #commonPool,R,r

    ##This function was the first design for the environment feedback  
    # def envFeedback (self, commonPool,currentPlayer, state = 0, choice = 0):
    #     point = 0
    #     round = self.rNum
    #     expectTarget = state * self.numPlayer + currentPlayer + 1
    #     currentRoound = state + 1 
    #     if (currentRoound != round) & (commonPool < self.target): 
    #         if commonPool < expectTarget:
    #             point = 0
    #         else :
    #             # print ("t0001:",(commonPool /(self.numPlayer*currentRoound)))
    #             point = 2 + (commonPool-expectTarget)*PsyPoint - choice
    #             # print ("winpoint",point)
    #     elif (currentRoound != round) & (commonPool >= self.target):
    #         point = 5
    #     #print ("sate" , state)
    #     #print ("Point", point)
        
    #     self.feedbackTable[choice][state].append(point)
        

    ## This is the feedback function which is used in this project.
    def newEnvFeedback(self,roundAchieved,choice,state,commonPool,totalContribute):
        point = 0 
        if roundAchieved:
            point = (BETA*commonPool)/3-totalContribute
            if point < 0:
                point = 0  
        # if roundAchieved:
        #     point= 4.5 - choice 
        else:
            point = 0
        # print ("sate" , state)
        # print ("Point", point)
        # if self.name=="2":
        #     print ("2 prop1",self.proportion1)
        #     print ("2 prop2",self.proportion2)

        #     print ("point",point )
        self.feedbackTable[choice][state].append(point)




    def updateTable (self):
        # feedff=np.zeros((3,self.rNum))
        
        for choice in range (3):
            for state in range (self.rNum):
                # print ("what is this ?",np.mean(np.mean(self.feedbackTable[choice][state])))
                # print ("what is that ?",np.mean(self.feedbackTable[choice][state]))
                # k = np.mean(self.feedbackTable[choice][state])
                self.table.iloc[state,choice] = np.mean(np.mean(self.feedbackTable[choice][state]))
    
## This is a probability table updated function 
    def updateTProprtion(self): 
        print ("name",self.name)
        stateProp=[0,0,0]
        for state in range (self.rNum):
            for choice in range (len(self.action)):
                stateProp[choice] = np.mean(self.feedbackTable[choice][state])
            total = sum (stateProp)
            print ("the stateProp is ", stateProp,"\n sum is ",total,"\n prop is ",stateProp[choice]/total)
            if ((total >stateProp[0]) and (total > stateProp[1]) and (total >stateProp[2]) ):
                stateProp[0] = stateProp[0]/total
                stateProp[1] = stateProp[1]/total
                stateProp[2] = 1.0-stateProp[0]-stateProp[1]
                
                self.tproprtion[state][0] = stateProp[0]
                self.tproprtion[state][1] = stateProp[1]
                self.tproprtion[state][2] = stateProp[2]
            else:
                print("passed,with all zero")
            
        print("The probability table of ",self.name ," is ",self.tproprtion)

## The function to build the look-up table 
    def buildQtable (self):
        self.table = pd.DataFrame(
            np.zeros ((self.rNum, len (self.action))),
            columns = self.action,
            )
        return self.table 

## A function to select the action from the look-up table
    def qChooseQAction (self,state):
        actionSate =  self.table.iloc[state, : ]
        if actionSate.all()==0 or (actionSate.sum()< 0.02):
            actionChoose = np.random.choice ([0,1,2],1,[0.9,0.05,0.05])[0]
            #actionsChoose =np.random.choice ([0,1,2],1,[0.3,0.2,0.5])[0] 
        else :
            # if np.random.random() > 0.99:
            #     actionChoose = actionSate.argmax()
            # else:
            #     actionChoose= np.random.choice ([0,1,2],1,[0.334,0.333,0.333])[0]
            actionChoose = actionSate.argmax()
        return actionChoose
    
    # def setProp (self,prop1=[0.4,0.4,0.2],prop2=[0.6,0.3,0.1]):
    #     self.proportion1 = prop1
    #     self.proportion2 = prop2

## the Probability table 
    def buildFeedBackTable(self):
        feedbackTable = np.zeros((len(self.action),self.rNum,1))
        arr = feedbackTable.tolist()
        self.feedbackTable = arr

## Learn model set function
    def setLearnModel (self,learn=True):
        self.learn = learn

## print the table to find the look-uptable 
    def printTable (self):
        print (self.table)
    def getTable (self):
        return self.table

        
    
        
