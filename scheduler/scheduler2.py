import random
import pickle

def LoadData(self):
     '''
         Loadn config data for schedule.
     '''
     with open('config/sched_data.pickle', 'rb') as conf_file:
          conf_data = pickle.load( conf_file )

     self.proc_num = conf_data['proc_num']
     self.task_num = conf_data['task_num']	


def SendToFile(self):
		'''Not very useful! Only for testing small problems!'''
		allPopList =[]
		with open(configFile.dataFName, mode='rb') as dFile:
			allPopList = picle.load(dFile)
		with open(configFile.dataFName, mode='wb') as dFile:
			picle.dump(allPopList ,dFile)	