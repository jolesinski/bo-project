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
    
    MutationOperators = [MutateQ, MutateA]
    CrossoverOperators = [Crossover]
    
    
    '''Params used in EvAlg'''
    MaxIterations = 100
    
    
    '''Fun used in EvAlg, defined outside to enable assigning other fun to them'''
    def initial(self):
        #return self.GeneratePopulation(self.popSize)
        return self.RandomPopulation()
                
    def assess(self, population):
        #return self.GoalFunctPop(population, self.timings)
        return [self.Fitness(sol) for sol in population]
                    
    def stopCondition(self, rating, t):
        return t >= Scheduler.MaxIterations

    def evolve(self, population):
        return self.Selection(population,4, 0.5)
        
    def bestFit(self, population, rating):
        maxIndex = min(enumerate(rating),key=lambda x: x[1])[0]
        return population[maxIndex]               
        
    def logData(self, population, rating, t):
        print(rating)
        print(t)
        
    
    #EA alg helper functions
    def Solve(self, iterations = 100):
        Scheduler.MaxIterations = iterations
        '''EvAlg similiar to that from slides'''
        def EvolutionaryAlgorithm():
            initial = self.initial
            assess = self.assess
            stopCondition = self.stopCondition
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


    