import game 
import matplotlib.pyplot as plt
import numpy as np

GEN = 10
TRAIN = 10
G = 1000 
N = 100
M = 10
class Simulation:
    def __init__(self):
        self.playGame = game.Game(N,M)
    
    def trainTable(self):
        self.playGame.learnModel(True)
        self.playGame.simulationModel(False)
        # risks = [i*(1/20) for i in range(21)]
        # payoffRisk = []
        # contributionRisk =[]
        # targetRisk =[]
        # firstHalf =[]
        # secondHalf = []
        for t in range(TRAIN):
            # self.playGame.iniEnvironment(0.9)
            print("Train Round:::::::::::::::::::::::::", t )
            # self.playGame.calculateType()
            # timesReachtarget = 0
            for i in range (G):
                print ("train #####",t)
                #self.playGame.train (0.9)
                self.playGame.newTrain(0.9)
        self.playGame.prepareForPlay()
    
    def evolutionaryDynamics1(self):
        self.playGame.learnModel(False)
        self.playGame.simulationModel(True)
        self.playGame.prepareForPlay()
        risks = [i*(1/20) for i in range(21)]
        payoffRisk = []
        contributionRisk =[]
        targetRisk =[]
        firstHalf =[]
        secondHalf = []

        for k in risks:
            self.playGame.iniEnvironment1(k,[0.25,0.25,0.5])
            self.playGame.collectInitial()
            print ("PRISK",k)
            ratioPayoff = []
            ratioTarget = []
            ratioContribution = [] 
            for g in range(GEN):
                print("Playing Generation", g )
                self.playGame.calculateType()
                timesReachtarget = 0
                for i in range (G):
                    timesReachtarget += self.playGame.play (k)
                
                # ratioPayoff.append (playGame.GetAveragePayoff()/(2*G))
                # ratioTarget.append (timesReachtarget / G)
                # ratioContribution.append (playGame.GetCommonPool()/(2*N))
                # payoffRisk.append(np.mean(ratioPayoff))
                self.playGame.printTable()
                # print (playGame.fitness)
                self.playGame.updateFitness()
                self.playGame.updatePopulation()

            self.playGame.collectTypeNum()
            print(self.playGame.numChange)
            # contributionRisk.append(np.mean(ratioContribution))
            # targetRisk.append(np.mean(ratioTarget))
            # firstHalf.append(np.mean(ratioContribution[:len(ratioContribution)//2]))
            # secondHalf.append(np.mean(ratioContribution[len(ratioContribution)//2:]))
        initialNum =self.playGame.numInitial
        finalNum = self.playGame.numChange
        strategyNum1 = self.playGame.num1
        strategyNum2 = self.playGame.num2
        strategyNum3 = self.playGame.num3
        # plt.plot(risks, payoffRisk, label="Payoff")
        # plt.plot(risks, contributionRisk, label="Contribution")
        # plt.plot(risks, targetRisk, label="Target")
        # plt.plot(risks, firstHalf, label="1st Half")
        # plt.plot(risks, secondHalf, label="2nd Half")
        # plt.xlabel('Risk Probability')
        # plt.ylabel('Proportion')
        # plt.title('Summary of the evolutionary dynamics in collective-risk dilemmas')
        # plt.legend()
        # plt.show()

        plt.plot(risks, strategyNum1, label="Strategy1")
        plt.plot(risks, strategyNum2, label="Strategy2")
        plt.plot(risks, strategyNum3, label="Strategy3")
        # plt.bar(risks, strategyNum1, alpha=0.9, width = 0.35, facecolor = 'lightskyblue', edgecolor = 'white', label='S1', lw=1)
        # plt.bar(risks+0.35, strategyNum2, alpha=0.9, width = 0.35, facecolor = 'yellowgreen', edgecolor = 'white', label='S2', lw=1)
        # plt.bar(risks+0.7, strategyNum2, alpha=0.9, width = 0.35, facecolor = 'yellowgreen', edgecolor = 'white', label='S2', lw=1)
        # plt.bar(range(len(risks)), strategyNum1, label='S1',fc = 'y')  
        # plt.bar(range(len(risks)), strategyNum2, bottom=strategyNum1, label='S2',tick_label = risks,fc = 'r')
        # plt.bar(range(len(risks)), strategyNum3, bottom=strategyNum2, label='S3',tick_label = risks,fc = 'lightskyblue')
        # plt.bar()
        plt.legend(loc="upper left")
        plt.xlabel('Risk Probability')
        plt.ylabel('Number')
        plt.show()

#_________________________________________________________
def main () :
    
    simulate = Simulation()
    simulate.trainTable()
    simulate.evolutionaryDynamics1()

if __name__ == '__main__':
    main()
