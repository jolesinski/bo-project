# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:59:28 2013

@author: Jakub
"""

import unittest
from scheduler.Scheduler import Scheduler
from scheduler.Task import Problem

class TestScheduler(unittest.TestCase):    
    
    def setUp(self):
        pass
    
    def assertHasSolutionType(self, solution):
        self.assertIsInstance(solution, list, 'sol not a list')
        self.assertIsInstance(solution[0], tuple, 'sol elems not a tuple')
        self.assertIsInstance(solution[0][1], list, 'sol has no proc lists')
        
    def assertHasPopulationType(self, population):
        self.assertIsInstance(population, list, 'pop not a list')
        self.assertHasSolutionType(population[0])
        
    
    def test_solve_returns_solution(self):
        sched = Scheduler(10)
        sol = sched.Solve()
        self.assertHasSolutionType(sol)
        
    def test_initial_returns_population(self):
        sched = Scheduler(10)
        pop = sched.initial()
        self.assertHasPopulationType(pop)
        
    def test_fitness_function(self):
        timings = (((1, 0), (2, 1)), ((2, 1), (4, 2)), ((3, 2), (6, 3)), ((4, 2), (8, 4)))
        problem = Problem(2, 4, timings)
        solution = [(0, [1, 1]), (1, [1, 1]), (3, [1, 1]), (2, [0, 1])]
        sched = Scheduler(10, problem)
        self.assertEqual(sched.Fitness(solution), 16)
        
    def test_mutate(self):
        sched = Scheduler(10)
        sol = sched.RandomSolution()
        mutant = sched.Mutate(sol)        
        different = 0
        for index, val in enumerate(sol):
            if mutant[index][0] != val[0]:
                different += 1
        if different == 0:
            for index, val in enumerate(sol):
                if mutant[index][1] != val[1]:
                    different += 2
        self.assertEqual(different, 2, "mutated solution schould have exactly two flipped elements")
            
        
if __name__ == '__main__':
    unittest.main()
    
    