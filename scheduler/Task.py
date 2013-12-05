# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 20:20:23 2013

@author: Jakub
"""

import random

class Problem:
    '''Class used to represent the scheduling problem.'''

    numProcMax = 100
    numTasksMax = 1000   
    taskTimingMax = 100

    def __init__(self, numProc = 4, numTasks = 5, timings = []):
     
        self.numProc = numProc
        self.numTasks = numTasks
        self.timings = timings
        
    def Random():
        random.seed()
        numProc = random.randint(1, Problem.numProcMax)
        numTasks = random.randint(1, Problem.numTasksMax)
        timings = [[[i3 for i3 in range(1, numProc)] for i2 in range(1, numProc)] for i1 in range(1, numTasks)]
        return Problem(numProc, numTasks, timings)
        
    Random = staticmethod(Random)