import random
import pickle


def Generate(self, taskStrct=None):
		'''If taskStrct == None, function creates random serialization:
		it buils task_list, which contains numbers from 1 to numTasks included.

		Then, in each iteration, chose one number from taskList, add this 
		to line list(line == one task, first element == number of task, others
		== attribution to target processors), remove from taskList(we don't
		want to make answer with the same task in many places) and generate 
		attribution(1 or 0) to each processor in nested loop. 

		At the end of each
		iteration we have complete task description in this serialization. We add 
		the line to task_struct, make line empty and take care of another task in
		next iteration. 


		If taskStrct != None, we use argument as taskStruct.'''

		if taskStrct == None:

			taskStruct=[] 
			taskList=[]
			line=[]
			random.seed()

			for num in range(1,self.numTasks+1):
				taskList.append(num)

			for lineN in range(1, self.numTasks+1):
				ch = random.choice(taskList)
				line.append(ch)
				taskList.remove(ch)
				for columnN in range(1, self.numProc+1):
					line.append(round(random.random()))
				taskStruct.append(tuple(line))
				line=[]

		else:
			taskStruct=taskStrct

		return taskStruct

def GeneratePopulation(self, popNum):
		'''Kom kom kom kommm...'''
		self.population = []
		for num in range(1,popNum+1):
			self.population.append(self.Generate())
		return self.population

		
			
def Crossover(self,anthr_ser):
		'''We take task order from one Serial object(self or anthr_ser) and processors
		attribution from second. To determinate, which parent will give what to child,
		we use round(random.random()), which can be 0 or 1. If is equal 0, then object, which
		called out the method gives task order and argument object gives processors attribution.
		Else it is inverted.'''

		random.seed()	

		if(round(random.random()) == 0):
			new_struct_i = anthr_ser.task_struct
			for line_num in range(1, config_file.numTasks+1):
				new_struct[line_num][0] = self.task_struct[line_num][0]
		else:
			new_struct_i = self.task_struct
			for line_num in range(1, config_file.numTasks+1):
				new_struct[line_num][0] = anthr_ser.task_struct[line_num][0]
		new_serial = Serial(new_struct_i)
		return new_serial
		
def MutateQ(self):
		'''Object will change randomly tasks order - two of the tasks will
		change their places. To achive this, we have to find, which two 
		task will take each others places. It is written in first_q and 
		second_q. We must ensure, that it is not the same task. We do 
		it in while loop. 

		We will change old task struct in new_struct_q.
		temp_fq remembers old task in first_q-th place of struct and 
		temp_sq remembers old task in second_q-th place of struct.
		We remove these from new_struct. 

		When changing their place we must 
		remember, that we should put in first element of bigger index, 
		because it will take place of the element of smaller index. If we 
		won't do that, we will put it in wrong places of new_struct_q!
		If - else instruction takes care of this part. 

		At the end we 
		create the object using new_struct_q and return it from
		function. In this way, we don't overwrite object, which called
		out function.'''

		first_q = random.randrange(1, config_file.numTasks+1)
		second_q = random.randrange(1, config_file.numTasks+1)

		while (second_q == first_q) or (config_file.numTasks==1):
			second_q = random.randrange(1, config_file.numTasks+1)
		
		new_struct_q = self.task_struct
		temp_fq = new_struct_q[first_q - 1]
		temp_sq = new_struct_q[second_q - 1]

		new_struct_q.remove(temp_fq)
		new_struct_q.remove(temp_sq)
		
		if first_q > second_q:
			new_queq.insert(second_q - 1, temp_fq)
			new_queq.insert(first_q - 1, temp_sq)
		else:
			new_queq.insert(first_q - 1, temp_sq)
			new_queq.insert(second_q - 1, temp_fq)
		new_serq = Serial(new_struct_q)
		return new_serq

def MutateA(self):
		'''Object will change processors attribution - two of the tasks will
		exchange their processors attribution. To achive this, we have to find, 
		which two tasks will exchange their processors attribution. It is 
		written in first_a and second_a. We must ensure, that it is not the same 
		task. We do it in while loop.

		We will change old task struct in new_struct_q.
		temp_fq remembers old task in first_q-th place of struct and 
		temp_sq remembers old task in second_q-th place of struct.
		We remove these from new_struct. However, there is one diference from 
		mutate_q - we don't want to change order of tasks, so we overwrite first 
		elements of temp_fa and temp_sa. In this way, even if we exchange position 
		of these two elements, tasks order will remain the same. 

		When changing their
		place we must remember, that we should put in first element of bigger index, 
		because it will take place of the element of smaller index. If we 
		won't do that, we will put it in wrong places of new_struct_a!
		If - else instruction takes care of this part. 

		At the end we 
		create the object using new_struct_a and return it from
		function. In this way, we don't overwrite object, which called
		out function.'''

		first_a = random.randrange(1, config_file.numTasks+1)
		second_a = random.randrange(1, config_file.numTasks+1)

		while (second_a == first_a) or (config_file.numTasks==1):
			second_a = random.randrange(1, config_file.numTasks+1)
		
		new_struct_a = self.task_struct
		temp_fa = new_struct_a[first_a - 1]
		new_assa.remove(temp_fa)
		temp_fa[0] = new_struct_a[second_a - 1][0]

		temp_sa = new_struct_a[second_a - 1]
		temp_sa[0] = new_struct_a[first_a - 1][0]
		new_assa.remove(temp_sa)
		
		if first_a > second_a:
			new_assa.insert(second_a - 1, temp_fa)
			new_assa.insert(first_a - 1, temp_sa)
		else:
			new_assa.insert(first_a - 1, temp_sa)
			new_assa.insert(second_a - 1, temp_fa)
		new_sera = Serial(self.task_queue,new_assa)
		return new_sera
	

def GoalFunct(self, tasks, answer):
		'''koooooomcia ni ma'''

		procArr=[]
		for taskI in range(0, self.numTasks):
			procArr[taskI]=CountBinary(answer[taskI][1])

		procAttrib=[]
		for taskI in range(0, self.numTasks):
			procAttrib[taskI]=tasks[answer[taskI][0]-1][procArr[taskI]-1]

		executeTime=[]
		for procI in range(0, self.numProc):
			executeTime[procI]=0

		notZeroFlags = []
		for taskI in range(0, self.numTasks):
			for procI in range(0, self.numProc):
				if answer[taskI][1][procI] == 0:
					notZeroFlag[procI]=0
				else:
					if procAttrib[taskI][procI] == -1:
						return Null
					else:
						executeTime[procI] = executeTime[procI] + procAttrib[taskI][procI]
						notZeroFlag[procI] = 1
			
			maxVal = 0
			for procI in range(0, self.numProc):
				if notZeroFlag[procI] and (maxVal<executeTime[procI]):
					maxVal=executeTime[procI]

			for procI in range(0, self.numProc):
				if notZeroFlag[procI]:
					executeTime[procI]=maxVal
		longest=0
		for procI in range(0, self.numProc):
			if longest<executeTime[procI]:
				longest=executeTime[procI]
		return longest
								
		


def GoalFunctPop(self, tasks):
		'''k'''
		self.goalVals = [GoalFunct(task, individual) for individual in self.population]
		return self.goalVals

def CountBinary(self, binList):
		'''Counts ones in a list.'''
		for index in range(0, len(binList)):
			sumOf1 =sumOf1+binList[index]
		return sumOf1
			
	


