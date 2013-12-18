from scheduler.Task import Problem


class Scheduler:
    '''Represents task scheduling process'''	
    from scheduler.scheduler1 import GeneratePopulation, Generate, Crossover
    from scheduler.scheduler1 import MutateQ, MutateA, GoalFunct, GoalFunctPop
    from scheduler.scheduler2 import LoadInputData, SaveGraphData, RandomSolution
    from scheduler.scheduler2 import RandomPopulation, Fitness, Selection
    from scheduler.scheduler2 import Mutate, Cross


    def __init__(self, popSize, problem = Problem.Random()):
        self.goalVals=[]
        self.popSize = popSize
        self.numProc = problem.numProc
        self.numTasks = problem.numTasks
        self.timings = problem.timings
        
        self.solution = self.RandomSolution()
        self.population = self.GeneratePopulation(popSize)
        
        '''log data from solver'''
        self.logFitness = []
    
    MutationOperators = [MutateQ, MutateA]
    CrossoverOperators = [Crossover]
    
    
    '''Params used in EvAlg'''
    MaxIterations = 100
    MaxIterStabilized = 500
    MaxKicks = 3
    
    
    '''Fun used in EvAlg, defined outside to enable assigning other fun to them'''
    def initial(self):
        #return self.GeneratePopulation(self.popSize)
        return self.RandomPopulation()
                
    def assess(self, population):
        #return self.GoalFunctPop(population, self.timings)
        return [self.Fitness(sol) for sol in population]
                    
    def stopCondition1(self, rating, t):
        return t >= Scheduler.MaxIterations

    def evolve(self, population):
        return self.Selection(population,4, 0.5)
        
    def bestFit(self, population, rating):
        maxIndex = min(enumerate(rating),key=lambda x: x[1])[0]
        return population[maxIndex]               
        
    def logData(self, population, rating, t):
        self.logFitness.append(rating)
        print(t)
    
    #EA alg helper functions
    def Solve(self, iterations = 100):
        Scheduler.MaxIterations = iterations
        '''EvAlg similiar to that from slides'''
        def EvolutionaryAlgorithm():
            initial = self.initial
            assess = self.assess
            stopCondition = self.stopCondition2
            evolve = self.evolve
            bestFit = self.bestFit
        
            t = 0
            self.population = initial()
            rating = assess(self.population)
            while not stopCondition(rating, t):
                t = t + 1
                self.population = evolve(self.population)
                rating = assess(self.population)
                self.logData(self.population, rating, t)
            return bestFit(self.population, rating)
            
            
        self.solution = EvolutionaryAlgorithm();        
        return self.solution

    def stopCondition2(self, rating, t):
        def kick(population, n):
            '''leaves n elems in pop, randomize others'''
            assert(n < len(population))
            return [pop if i < n else self.RandomSolution() for i, pop in enumerate(population)]
                    
        best = min(rating)
        if t == 0 or best < self.bestSoFar:
            self.bestSoFar = best
            self.tStabilized = 0
            self.kicks = 0
        else:
            self.tStabilized = self.tStabilized + 1
            
        if self.tStabilized > Scheduler.MaxIterStabilized:
            self.kicks = self.kicks + 1;
            self.population = kick(self.population, self.popSize - 2)
            
        return self.kicks >= Scheduler.MaxKicks
    