import random
import config_file

class Serial:
	'''Represents serialization of all specified tasks'''
	
	def __init__(self, task_strct=None):
		'''If task_strct == None, function creates random serialization:
		it buils task_list, which contains numbers from 1 to task_num included.

		Then, in each iteration, chose one number from task_list, add this 
		to line list(line == one task, first element == number of task, others
		== attribution to target processors), remove from task_list(we don't)
		want to make answer with the same task in many places) and generate 
		attribution(1 or 0) to each processor in nested loop. 

		At the end of each
		iteration we have complete task description in this serialization. We add 
		the line to task_struct, make line empty and take care of another task in
		next iteration. 


		If task_strct != None, we use argument as task_struct.'''

		if task_strct == None:

			self.task_struct=[] 
			task_list=[]
			line=[]
			random.seed()

			for num in range(1,config_file.task_num+1):
				task_list.append(num)

			for line_n in range(1, config_file.task_num+1):
				ch = random.choice(task_list)
				line.append(ch)
				task_list.remove(ch)
				for column_n in range(1, config_file.proc_num+1):
					line.append(round(random.random()))
				self.task_struct.append(line)
				line=[]

		else:
			self.task_struct=task_strct
			
	def inherit(self,anthr_ser):
		'''We take task order from one Serial object(self or anthr_ser) and processors
		attribution from second. To determinate, which parent will give what to child,
		we use round(random.random()), which can be 0 or 1. If is equal 0, then object, which
		called out the method gives task order and argument object gives processors attribution.
		Else it is inverted.'''

		random.seed()	

		if(round(random.random()) == 0):
			new_struct_i = anthr_ser.task_struct
			for line_num in range(1, config_file.task_num+1):
				new_struct[line_num][0] = self.task_struct[line_num][0]
		else:
			new_struct_i = self.task_struct
			for line_num in range(1, config_file.task_num+1):
				new_struct[line_num][0] = anthr_ser.task_struct[line_num][0]
		new_serial = Serial(new_struct_i)
		return new_serial
		
	def mutate_q(self):
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

		first_q = random.randrange(1, config_file.task_num+1)
		second_q = random.randrange(1, config_file.task_num+1)

		while (second_q == first_q) or (config_file.task_num==1):
			second_q = random.randrange(1, config_file.task_num+1)
		
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

	def mutate_a(self):
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

		first_a = random.randrange(1, config_file.task_num+1)
		second_a = random.randrange(1, config_file.task_num+1)

		while (second_a == first_a) or (config_file.task_num==1):
			second_a = random.randrange(1, config_file.task_num+1)
		
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