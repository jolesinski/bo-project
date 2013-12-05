import random
import pickle

class Scheduler:
    '''Represents task scheduling process'''	
    from scheduler.scheduler1 import GeneratePopulation, Generate
    from scheduler.scheduler2 import LoadData, SaveData

    def __init__(self, popSize):
        self.LoadData()
        self.goalVals=[]
        
        self.numTasks =10
        self.numProc = 11
        
        
        self.population = self.GeneratePopulation(popSize)