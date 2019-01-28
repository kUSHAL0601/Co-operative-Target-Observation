from ObserverClass import ObserverClass as O
from TargetsClass import TargetsClass as T
from random import randint as RI
from random import random as R
from LP_CTO import LP_CTO
from BRLP_CTO import BRLP_CTO
from reward import reward
from copy import deepcopy

def mean(arr):
	n=len(arr)
	return sum(arr)/len(arr)

class CentralizedComm:
	def __init__(self):
		self.no_observers_arr=[2,6,10,14,18,20,50]
		self.no_targets_arr=[3,9,15,21,27,50,100]
		self.x_limit=150
		self.y_limit=150
		self.target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
		self.observer_speed=1.0
		self.sensor_range=[5,10,15,20,25]
		self.total_steps=1500
		self.update_steps=10
		observer_target_dict={}
		self.template_probability_distribution=[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5]

	def initialize(self):
		targets=[]
		observers=[]
		no_targets=self.no_targets_arr[RI(0,4)]
		no_observers=self.no_observers_arr[RI(0,4)]
		sensor_range_targets=self.sensor_range[RI(0,4)]
		sensor_range_observers=self.sensor_range[RI(0,4)]
		for i in range(no_targets):
			targets.append(T(R()*150,R()*150,self.target_speed[RI(0,5)],R()*360,sensor_range_observers))
		for i in range(no_observers):
			observers.append(O(R()*150,R()*150,self.observer_speed,sensor_range_targets))
		return (no_targets,no_observers,targets,observers)

	def initialize_param(self,no_targets,no_observers,sensor_range_targets,sensor_range_observers):
		targets=[]
		observers=[]
		for i in range(no_targets):
			targets.append(T(R()*150,R()*150,self.target_speed[RI(0,5)],R()*360,sensor_range_observers))
		for i in range(no_observers):
			observers.append(O(R()*150,R()*150,self.observer_speed,sensor_range_targets))
		return (no_targets,no_observers,targets,observers)

	def update_for_observers(self,observers,targets):
		temp_dict={}
		for i in range(len(observers)):
			temp_dict[i]=[]
		for i in range(len(observers)):
			for j in range(len(targets)):
				if(observers[i].enemy_in_range(targets[j])):
					temp_dict[i].append(j)
		return temp_dict

	def update_for_targets(self,observers,targets):
		temp_dict={}
		for i in range(len(targets)):
			temp_dict[i]=[]
		for i in range(len(targets)):
			for j in range(len(observers)):
				if(targets[i].observer_in_range(observers[j])):
					temp_dict[i].append(j)
		return temp_dict

	def run(self,no_targets,no_observers,targets,observers,threshold):
		step=0
		count=0
		data_until_update=[]
		central_unit={}
		while(step<=self.total_steps):
			if(step%self.update_steps==0):
				observer_target_dict=self.update_for_observers(observers,targets)
				target_observer_dict=self.update_for_targets(observers,targets)
				central_unit=observer_target_dict
				targets_included={}
				for i in range(no_targets):
					targets_included[i]=0
				for i in observer_target_dict:
					temp_arr_x=[]
					temp_arr_y=[]
					temp_targets_included_count=0
					for j in observer_target_dict[i]:
						temp_targets_included_count+=targets_included[j]
					for j in observer_target_dict[i]:
						temp_arr_x.append(targets[j].x)
						temp_arr_y.append(targets[j].y)
					if(len(temp_arr_x) and len(temp_arr_y)):
						if((temp_targets_included_count/len(temp_arr_x))>=threshold):
							observers[i].update_target(1,1,self.x_limit,self.y_limit,0,0)
							# print("Exploring")
						else:
							mean_x=mean(temp_arr_x)
							mean_y=mean(temp_arr_y)
							explore=pow(1/(len(observer_target_dict[i])+1),2)
							rwrd=reward(observers[i],targets,observer_target_dict[i],self.x_limit,self.y_limit,explore,mean_x,mean_y)
							E_min=LP_CTO(rwrd,1.0,self.template_probability_distribution)[0]
							alpha=BRLP_CTO(rwrd,self.template_probability_distribution,E_min)
							observers[i].update_target(alpha,explore,self.x_limit,self.y_limit,mean_x,mean_y)
							for j in observer_target_dict[i]:
								targets_included[j]=1
					else:
						max_len=1
						max_i=-1
						for i in range(len(observers)):
							if(len(central_unit[i])>=max_len):
								max_len=len(central_unit[i])
								max_i=i
						if(max_i!=-1):
							observers[i].update_target(1,0,self.x_limit,self.y_limit,observers[max_i].x,observers[max_i].y)
						else:
							observers[i].update_target(1,1,self.x_limit,self.y_limit,0,0)

				for i in target_observer_dict:
					temp_arr_x=[]
					temp_arr_y=[]
					for j in target_observer_dict[i]:
						temp_arr_x.append(observers[j].x)
						temp_arr_y.append(observers[j].y)
					if(len(temp_arr_x) and len(temp_arr_y)):
						mean_x=mean(temp_arr_x)
						mean_y=mean(temp_arr_y)
						targets[i].update_target(self.x_limit,self.y_limit,mean_x,mean_y)

			for i in observers:
				i.update(self.x_limit,self.y_limit)
			for i in targets:
				i.update(self.x_limit,self.y_limit)
			tmp_observer_target_dict=self.update_for_observers(observers,targets)
			tmp_arr=[]
			for i in tmp_observer_target_dict:
				for j in tmp_observer_target_dict[i]:
					if(j not in tmp_arr):
						tmp_arr.append(j)
			# print("Observers observed in "+str(step)+"is "+str(len(tmp_arr)))
			count+=len(tmp_arr)
			step+=1
		return count

	def demo(self):
		no_targets,no_observers,targets,observers=self.initialize()
		sorted_observers=sorted(observers,key=lambda x: x.limit)
		count_new=self.run(no_targets,no_observers,targets,sorted_observers,0.3)
		return count_new