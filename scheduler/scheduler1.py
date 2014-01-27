import numpy.random as random
from scheduler.scheduler2 import RandomSolution


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
		

def GoalFunct(self, tasks, answer):
		'''koooooomcia ni ma'''

		procArr=[]
		for taskI in range(0, self.numTasks):
			procArr[taskI]=sum(answer[taskI][1])

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
					notZeroFlags[procI]=0
				else:
					if procAttrib[taskI][procI] == -1:
						return None
					else:
						executeTime[procI] = executeTime[procI] + procAttrib[taskI][procI]
						notZeroFlags[procI] = 1
			
			maxVal = 0
			for procI in range(0, self.numProc):
				if notZeroFlags[procI] and (maxVal<executeTime[procI]):
					maxVal=executeTime[procI]

			for procI in range(0, self.numProc):
				if notZeroFlags[procI]:
					executeTime[procI]=maxVal
		longest=0
		for procI in range(0, self.numProc):
			if longest<executeTime[procI]:
				longest=executeTime[procI]
		return longest
								
		


def GoalFunctPop(self, population, tasks):
		'''k'''
		self.goalVals = [self.GoalFunct(tasks, individual) for individual in population]
		return self.goalVals
			
	
def Cross2(self, parent1, parent2):
    '''Little faster Cross'''
    kid1 = parent1.copy()
    kid2 = parent2.copy()   
    for i in range(self.numTasks):
        kid1[i] = (kid1[i][0], kid2[i][1])
    return kid1
    
def Cross3(self, parent1, parent2):
    '''Completly random - if we want to go out from stabilized point.'''
    return RandomSolution(self)
    
def Cross4(self, parent1, parent2):
    '''tasks order - random, process assignment nand-ed.
        Thanks to that kid don't resemble parents(in real
        world it would be a little confusing).'''
    kid1 = parent1.copy()
    kid2 = parent2.copy()     
    orderedTasks = random.permutation(range(self.numTasks))
    
    for i in range(self.numTasks):
        for j in range(self.numProc):
            kid1[i][1][j] = int(not(kid1[i][1][j] & kid2[i][1][j]))
        kid1[i] = (orderedTasks[i], kid1[i][1])
    return kid1
    
def Cross5(self, parent1, parent2, similar = 0.5):
    '''Completly random - if we want to go out from stabilized point.'''
    randomKid = RandomSolution(self)
    
    def Similarity(entity1, entity2):
        '''Checks similarity of 2 entities. Takes value
            from 0 to 1. When 1, entity1 == entity2.'''
        copy1 = entity1.copy()
        copy2 = entity2.copy()

        tasksEq = 0
        procsEq = 0
        for i in range(self.numTasks):
            for j in range(self.numProc):
                procsEq+=int(copy1[i][1][j]==copy2[i][1][j])
                tasksEq+=int(copy1[i][0]==copy2[i][0])
        return tasksEq/self.numTasks+procsEq/(self.numTasks*self.numProc)
        
    while (Similarity(parent1,randomKid)>similar)or(Similarity(randomKid,parent2)>similar):
        randomKid = RandomSolution(self)
    return randomKid
    
def Mutate_A(self, parent, epsilon = 0.5, fill = 0.5, changeProb = 0.8):
    kid = parent.copy()
    if random.rand() > epsilon:
        (i, j) = random.choice(range(len(parent)), 2, False)
        kid[i] = parent[j]
        kid[j] = parent[i]
    else:
        i = random.randint(len(parent))
        j = random.randint(self.numProc)
        temp = kid[i][1].copy()
        if sum(temp)< fill * self.numProc:
            if random.rand() < changeProb:
                temp[j] |= 1
            else:
                if(sum(temp)!=1):
                    temp[j] &= 0
        else:
            if random.rand() < changeProb:
                if(sum(temp)!=1):
                    temp[j] &= 0
            else:
                temp[j] |= 1    
        kid[i] = (kid[i][0], temp)
    return kid
    
def Mutate_B(self, parent, epsilon = 0.5, fill = 0.5, changeProb = 0.8):
    kid = parent.copy()
    if random.rand() > epsilon:
        (i, j) = random.choice(range(len(parent)), 2, False)
        kid[i] = parent[j]
        kid[j] = parent[i]
    else:
        i = random.randint(len(parent))
        j = random.randint(self.numProc)
        temp = kid[i][1].copy()
        if sum(temp)< fill * self.numProc:
            if random.rand() < changeProb:
                while((temp[j]==1) and (sum(temp)!=self.numProc)):
                    j = random.randint(self.numProc)
                temp[j] |= 1
            else:
                temp[j] &= 0
                if sum(temp) == 0:
                    j = random.randint(self.numProc)
                    temp[j] |= 1
        else:
            if random.rand() < changeProb:
                temp[j] &= 0
                if sum(temp) == 0:
                    j = random.randint(self.numProc)
                    temp[j] |= 1
            else:
                while((temp[j]==1) and (sum(temp)!=self.numProc)):
                    j = random.randint(self.numProc)
                temp[j] |= 1
                
        kid[i] = (kid[i][0], temp)
    #\assert(kid[i][1] != parent[i][1])
    return kid

def Mutate_C(self, parent, epsilon = 0.5, changeProb = 0.8):
    kid = parent.copy()
    if random.rand() > epsilon:
        (i, j) = random.choice(range(len(parent)), 2, False)
        kid[i] = parent[j]
        kid[j] = parent[i]
    else:
        together=0
        for x in range(0, len(parent)):
            together+=sum(kid[x][1])
        average = together/(self.numProc)
        i = random.randint(len(parent))
        j = random.randint(self.numProc)
        temp = kid[i][1].copy()
        if sum(temp)< average:
            if random.rand() < changeProb:
                temp[j] |= 1
            else:
                if(sum(temp)!=1):
                    temp[j] &= 0
        else:
            if random.rand() < changeProb:
                if(sum(temp)!=1):
                    temp[j] &= 0
            else:
                temp[j] |= 1    
        kid[i] = (kid[i][0], temp)
    #\assert(kid[i][1] != parent[i][1])
    return kid

def Mutate_D(self, parent, epsilon = 0.5, changeProb = 0.8):
    kid = parent.copy()
    if random.rand() > epsilon:
        (i, j) = random.choice(range(len(parent)), 2, False)
        kid[i] = parent[j]
        kid[j] = parent[i]
    else:
        together=0
        for x in range(0, len(parent)):
            together+=sum(kid[x][1])
        average = together/(self.numProc)
        i = random.randint(len(parent))
        j = random.randint(self.numProc)
        temp = kid[i][1].copy()
        if sum(temp)< average:
            if random.rand() < changeProb:
                while((temp[j]==1) and (sum(temp)!=self.numProc)):
                    j = random.randint(self.numProc)
                temp[j] |= 1
            else:
                temp[j] &= 0
                if sum(temp) == 0:
                    j = random.randint(self.numProc)
                    temp[j] |= 1
        else:
            if random.rand() < changeProb:
                temp[j] &= 0
                if sum(temp) == 0:
                    j = random.randint(self.numProc)
                    temp[j] |= 1
            else:
                while((temp[j]==1) and (sum(temp)!=self.numProc)):
                    j = random.randint(self.numProc)
                temp[j] |= 1
                
        kid[i] = (kid[i][0], temp)
    #\assert(kid[i][1] != parent[i][1])
    return kid