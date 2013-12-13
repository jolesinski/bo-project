# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:48:50 2013

@author: Jakub
"""

from  scheduler.Scheduler import Scheduler
import main_data

def main():
    print('initializing...')
    sched = Scheduler(10)
    print('solving...')
    sched.solution = sched.Solve(iterations = 1000)
    print('Cmax:')
    print(sched.Fitness(sched.solution))
    print('saving...')
    sched.SaveGraphData()
    print('calling gui...')
    main_data.main()    

if __name__ == '__main__':
    main()