import random
import pickle

def LoadData(self):
     '''Loading config data for scheduling'''
     with open('config/sched_data.pickle', 'rb') as conf_file:
          conf_data = pickle.load( conf_file )

     self.proc_num = conf_data['proc_num']
     self.task_num = conf_data['task_num']	


def SendToFile(self):
		'''Save fitness func to file'''
		with open(configFile.dataFName, mode='rb') as dFile:
			allPopList = pickle.load(dFile)