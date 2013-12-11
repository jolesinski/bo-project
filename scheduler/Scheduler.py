from scheduler.Task import Problem


class Scheduler:
    '''Represents task scheduling process'''	
    from scheduler.scheduler1 import GeneratePopulation, Generate, Crossover
    from scheduler.scheduler1 import MutateQ, MutateA, GoalFunct, GoalFunctPop
    from scheduler.scheduler2 import LoadInputData, SaveGraphData, RandomSolution
    from scheduler.scheduler2 import RandomPopulation, Fitness


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
    
    
    '''Fun used in EvAlg, defined outside to enable assigning other fun to them'''
    def initial(self):
        #return self.GeneratePopulation(self.popSize)
        return self.RandomPopulation()
                
    def assess(self, population):
        #return self.GoalFunctPop(population, self.timings)
        return [1 for p in population]
                    
    def stopCondition(self, rating):
        return True        

    def evolve(self, population):
        return population        
        
    def bestFit(self, population, rating):
        maxIndex = max(enumerate(rating),key=lambda x: x[1])[0]
        return population[maxIndex]           
    
    
    
    
    #EA alg helper functions
    def Solve(self):
        '''EvAlg similiar to that from slides'''
        def EvolutionaryAlgorithm():
            initial = self.initial
            assess = self.assess
            stopCondition = self.stopCondition
            evolve = self.evolve
            bestFit = self.bestFit
        
            self.population = initial()
            rating = assess(self.population)
            while not stopCondition(rating):
                self.population = evolve(self.population)
                rating = assess(self.population)
            return bestFit(self.population, rating)
            
            
        self.solution = EvolutionaryAlgorithm();        
        return self.solution


    