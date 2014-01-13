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
    popSize = 20
    sched = Scheduler(popSize, prob)    
#    print('generating random solution...')
#    sched.solution = sched.RandomSolution()
    sched.setSelectionParams()
    n = 10
    print('solving...')
    for u in range(2,10):
        averIters = 0
        averCmax = 0
        sched.setSelectionParams(u)
        print('---------------------------------------')
        print('ParentsInNewPop = {0}'.format(u))        
        for i in range(n):
            sched.solution = sched.Solve(iterations = 5000)
            cmax = sched.Fitness(sched.solution)
            averCmax += cmax/n
            iters = sched.lastIters
            averIters += iters/n
            print('Try {0}: Algorithm took {1} iterations'.format(i, iters) +
            ' with Cmax: {0}'.format(cmax))
        print('In {0} tries, algorithm took on average {1} iterations'.format(n, round(averIters)))
        print('with average Cmax: {0}'.format(averCmax))
    print('saving...')
#    sched.SaveGraphData()
    print('calling gui...')
#    main_data.main()    

if __name__ == '__main__':
    main()