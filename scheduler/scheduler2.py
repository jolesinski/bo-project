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