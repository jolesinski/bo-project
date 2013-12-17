# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 20:20:23 2013

@author: Jakub
"""

import random
import os
import pickle

class Problem:
    '''Class used to represent the scheduling problem.'''

    '''as we have 3 dimensional task_data, bigger problems
    get untractable, ex: numProc = 44, numTasks = 259
    we get 44*44*259 > 0.5 milion entries to task_data'''
    numProcMax = 20
    numTasksMax = 100   
    taskTimingMax = 100

    def __init__(self, numProc = 4, numTasks = 5, timings = []):
     
        self.numProc = numProc
        self.numTasks = numTasks
        self.timings = timings
        
    def Save(self):
        problemData = {'numProc': self.numProc, 'numTasks': self.numTasks, 'timings': self.timings}        
        
        path = os.path.dirname(__file__)
        path = os.path.join(os.path.dirname(path), 'config/problem_data.pickle')
        
        with open(path, mode='wb') as dFile:
            pickle.dump(problemData, dFile)
            
    def Load():        
        path = os.path.dirname(__file__)
        path = os.path.join(os.path.dirname(path), 'config/problem_data.pickle')

        with open(path, mode='rb') as dFile:
            problemData = pickle.load(dFile)
            
        numProc = problemData['numProc']
        numTasks = problemData['numTasks']
        timings = problemData['timings']
        
        return Problem(numProc, numTasks, timings)
        
    def Random(numProc = random.randint(1, numProcMax),
               numTasks = random.randint(1, numTasksMax)):
                   
        random.seed()
        
        def byParallelization(task):
            '''for now it simply divides the single-threaded
            execution time by the number of threads'''            
            return tuple(byProcessor(task, i) for i in range(1,numProc+1))
        def byProcessor(task, paral):
            '''for now it simply takes processor id
            multiplied by task id as single-threaded exec time'''
            return tuple(round(((i*task) % Problem.taskTimingMax)/paral) for i in range(1, numProc+1))
            
        '''generate task_data["timings"]'''            
        timings = tuple(byParallelization(i) for i in range(1, numTasks+1))

        return Problem(numProc, numTasks, timings)
        
    Random = staticmethod(Random)