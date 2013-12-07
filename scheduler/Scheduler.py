from scheduler.Task import Problem

class Scheduler:
    '''Represents task scheduling process'''	
    from scheduler.scheduler1 import GeneratePopulation, Generate
    from scheduler.scheduler2 import LoadInputData, SaveGraphData, RandomSolution

    def __init__(self, popSize, problem = Problem.Random()):
        self.goalVals=[]
        
        self.numProc = problem.numProc
        self.numTasks = problem.numTasks
        self.timings = problem.timings
        
        self.solution = self.RandomSolution()
        self.population = self.GeneratePopulation(popSize)