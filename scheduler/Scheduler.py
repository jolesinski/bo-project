import random
import pickle

class Scheduler:
    '''Represents task scheduling process'''	
    from scheduler.scheduler1 import GeneratePopulation, Generate
    from scheduler.scheduler2 import LoadData

    def __init__(self, popSize):
        self.LoadData()
        self.goalVal=[]
        self.numTasks =10
        self.numProc = 11

        self.population = self.GeneratePopulation(popSize)