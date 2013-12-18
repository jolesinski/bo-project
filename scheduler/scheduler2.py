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
    def median(mylist):
        sorts = sorted(mylist)
        length = len(sorts)
        if not length % 2:
            return (sorts[int(length / 2)] + sorts[int(length / 2) - 1]) / 2
        return sorts[int(length / 2)]    
    
    
    logBest = [min(fit) for fit in self.logFitness] 
    logMedian = [median(fit) for fit in self.logFitness]
    
    path = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(path), 'config/graph_data.pickle')

    with open(path, mode='rb') as dFile:
        graphData = pickle.load(dFile)
        
    graphData['solution_data'] = self.solution
    graphData['task_data'] = {'task_num':self.numTasks,'proc_num':self.numProc,'timings':self.timings}
    graphData['fitness_data'] = [logBest, logMedian]    
    
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
        
def Selection(self, population, u, epsilon = 0.5):
    '''Sort population wrt fitness, take u for mutation, cross the rest'''
    population = sorted(population, key = lambda sol: self.Fitness(sol))
    parents = population[:u]
    kids = []
    
    
    for index, parent in enumerate(population):
        if len(kids) < len(population) - u: 
            if random.rand() > epsilon:
                kids.append(self.Mutate(parent, 0.5))
            else:
                kids.append(self.Cross(parent, population[index+1]))
    parents.extend(kids)
    return parents
    
def Mutate(self, parent, epsilon = 0.5):
    kid = parent.copy()
    if random.rand() > epsilon:
        (i, j) = random.choice(range(len(parent)), 2, False)
        kid[i] = parent[j]
        kid[j] = parent[i]
    else:
        i = random.randint(len(parent))
        j = random.randint(self.numProc)
        temp = kid[i][1].copy()
        temp[j] ^= 1
        if sum(temp) == 0:
            j = random.randint(self.numProc)
            temp[j] ^= 1
        kid[i] = (kid[i][0], temp)
        #\assert(kid[i][1] != parent[i][1])
    return kid
    
def Cross(self, parent1, parent2):
    kid1 = parent1.copy()
    kid2 = parent2.copy()   
    for i in range(self.numTasks):
        kid1[i] = (kid1[i][0], parent2[i][1])
        kid2[i] = (kid2[i][0], parent1[i][1])
    return kid1