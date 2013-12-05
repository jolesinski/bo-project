import random
import os
import pickle

def LoadData(self):
     '''Loading config data for scheduling'''
     with open('config/sched_data.pickle', 'rb') as conf_file:
          conf_data = pickle.load( conf_file )

     self.proc_num = conf_data['proc_num']
     self.task_num = conf_data['task_num']	


def SaveData(self):
    '''Save fitness func to file'''
    
    
    path = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(path), 'config/graph_data.pickle')

    graphData = dict()
    graphData['fitness_data'] = [[],[]]
    graphData['solution_data'] = self.Generate()
    graphData['task_data'] = ...
    graphData['population_data'] = ...

    with open(path, mode='rb') as dFile:
        pickle.dump(graphData, dFile)