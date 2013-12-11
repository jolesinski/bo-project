import numpy.random as random
import os
import pickle

def LoadInputData(self, problem):
     '''Loading scheduler input data
     from generated problem'''

     self.numProc = problem.numProc
     self.numTasks = problem.numTasks
     self.timings = problem.timings


def SaveGraphData(self):
    '''Save fitness func to file'''
    
    
    path = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(path), 'config/graph_data.pickle')

    with open(path, mode='rb') as dFile:
        graphData = pickle.load(dFile)
        
    graphData['solution_data'] = self.solution
    graphData['task_data'] = {'task_num':self.numTasks,'proc_num':self.numProc,'timings':self.timings}

    with open(path, mode='wb') as dFile:
        pickle.dump(graphData, dFile)
        
        
def RandomSolution(self):
    '''Generates random feasible solution'''
    random.seed()
    taskIds = range(self.numTasks)
    procIds = range(self.numProc)
    orderedTasks = random.permutation(taskIds)
    
    def assignProc():
        parallelization = random.randint(1,self.numProc+1)
        procChoice = random.choice(range(self.numProc), parallelization)
        binarized = [ 1 if proc in procChoice else 0 for proc in procIds]
        return binarized
        
    return [(task, assignProc()) for task in orderedTasks]
    
def RandomPopulation(self):    
    '''Generates a population of random feasible solutions'''
    return [self.RandomSolution() for i in range(self.popSize)]
    
def Fitness(self, solution):
    '''Calculates fitnes of a given solution'''
    taskIds = list(range(self.numTasks))
    procIds = list(range(self.numProc))
    
    c = [0 for procId in procIds]
    for task in solution:
        taskId = task[0]
        procList = task[1]
        parallelization = sum(procList)
        synchronizationTime = 0;
        for procId in procIds:
            if procList[procId] == 1:
                c[procId] += self.timings[taskId][parallelization-1][procId]
                if(c[procId] > synchronizationTime):
                    synchronizationTime = c[procId]
        for procId in procIds:
            if procList[procId] == 1:
                if(c[procId] < synchronizationTime):
                    c[procId] = synchronizationTime
    return max(c)
        