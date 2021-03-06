import numpy.random as random
import os
import pickle
import time

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
    logWorst = [max(fit) for fit in self.logFitness]

    dirPath = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(dirPath), 'config/graph_data.pickle')

    try:
        with open(path, mode='rb') as dFile:
            graphData = pickle.load(dFile)
    except IOError:
        path2 = os.path.join(os.path.dirname(dirPath), 'config/palette_data.pickle')
        with open(path2, mode='rb') as dFile:
            graphData = pickle.load(dFile)

    graphData['solution_data'] = self.solution
    graphData['task_data'] = {'task_num':self.numTasks,'proc_num':self.numProc,'timings':self.timings}
    graphData['fitness_data'] = [logBest, logMedian, logWorst]
    graphData['population_data'] = self.logPopulationData

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

def setSelectionParams(self, parentsInNewPop = 0.2, mutationProb = 0.5):
    self.parentsInNewPop = int(parentsInNewPop * self.popSize)
    self.mutationProb = mutationProb

def Selection(self, population, u, epsilon = 0.5):
    '''Sort population wrt fitness, take u for mutation, cross the rest'''
    population = sorted(population, key = lambda sol: self.Fitness(sol))
    parents = population[:u]
    kids = []

    #logging for 'population_data'
    logFeasible = [0,0]
    logInfeasible = [0,0]
    logExecTime = [0,0]
    opType = -1

    for index, parent in enumerate(population):
        if len(kids) < len(population) - u:
            while True: #do-while loop
                if random.rand() > epsilon:
                    t = time.time()
                    child = self.Mutate(parent, 0.5)
                    execTime = time.time() - t
                    opType = 0
                else:
                    t = time.time()
                    child = self.Cross(parent, population[index+1])
                    execTime = time.time() - t
                    opType = 1

                logExecTime[opType] += execTime
                if IsFeasible(child): #stop condition
                    logFeasible[opType] += 1
                    break
                else:
                    logInfeasible[opType] += 1

            kids.append(child)

    popStats = {'mutation_op':[logFeasible[0], logInfeasible[0], logExecTime[0]],
                'crossover_op':[logFeasible[1], logInfeasible[1], logExecTime[1]]}
    self.logPopulationData.append(popStats)

    parents.extend(kids)
    return parents

def IsFeasible(solution):
    return True

def Mutate1(self, parent, epsilon = 0.5):
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

def Cross1(self, parent1, parent2):
    kid1 = parent1.copy()
    kid2 = parent2.copy()
    for i in range(self.numTasks):
        kid1[i] = (kid1[i][0], parent2[i][1])
        kid2[i] = (kid2[i][0], parent1[i][1])
    return kid1

