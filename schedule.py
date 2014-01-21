# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:48:50 2013

@author: Jakub
"""

from  scheduler.Scheduler import Scheduler
from  scheduler.Task import Problem

import main_data

def main():
#    print('problem generation...')
#    prob = Problem.Random(4, 25)
#    print('saving problem data...')
#    prob.Save()
    print('loading problem data...')
    prob = Problem.Load()    
    print('initializing scheduler...')
    sched = Scheduler(20, prob)  
#    print('generating random solution...')
#    sched.solution = sched.RandomSolution()
    print('solving...')
    sched.solution = sched.Solve(iterations = 5000)
    print('Cmax:')
    print(sched.Fitness(sched.solution))
    print('saving...')
    sched.SaveGraphData()
    print('calling gui...')
    main_data.main()    

if __name__ == '__main__':
    main()