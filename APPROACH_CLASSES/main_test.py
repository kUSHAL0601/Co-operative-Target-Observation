from ObserverClass import ObserverClass as O
from TargetsClass import TargetsClass as T
from random import randint as RI
from random import random as R
from LP_CTO import LP_CTO
from BRLP_CTO import BRLP_CTO
from reward import reward

def mean(arr):
	n=len(arr)
	return sum(arr)/len(arr)

class Main:
	def __init__(self):
		self.no_observers_arr=[2,6,10,14,18]
		self.no_targets_arr=[3,9,15,21,27]
		self.x_limit=150
		self.y_limit=150
		self.target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
		self.observer_speed=1.0
		self.sensor_range=[5,10,15,20,25]
		self.total_steps=1500
		self.update_steps=10
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

	def initialize_param(self,no_targets,no_observers,sensor_range_targets,sensor_range_observers,target_spd):
		targets=[]
		observers=[]
		for i in range(no_targets):
			targets.append(T(R()*150,R()*150,target_spd,R()*360,sensor_range_observers))
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

	def run(self,no_targets,no_observers,targets,observers):
		step=0
		total_count=0
		data_until_update=[]
		while(step<=self.total_steps):
			if(step%self.update_steps==0):
				observer_target_dict=self.update_for_observers(observers,targets)
				target_observer_dict=self.update_for_targets(observers,targets)
				for i in observer_target_dict:
					temp_arr_x=[]
					temp_arr_y=[]
					for j in observer_target_dict[i]:
						temp_arr_x.append(targets[j].x)
						temp_arr_y.append(targets[j].y)
					if(len(temp_arr_x) and len(temp_arr_y)):
						mean_x=mean(temp_arr_x)
						mean_y=mean(temp_arr_y)
						explore=pow(1/(len(observer_target_dict[i])+1),2)
						rwrd=reward(observers[i],targets,observer_target_dict[i],self.x_limit,self.y_limit,explore,mean_x,mean_y)
						E_min=LP_CTO(rwrd,1.0,self.template_probability_distribution)[0]
						alpha=BRLP_CTO(rwrd,self.template_probability_distribution,E_min)
						observers[i].update_target(alpha,explore,self.x_limit,self.y_limit,mean_x,mean_y)
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
			observer_target_dict=self.update_for_observers(observers,targets)
			for i in observer_target_dict:
				total_count+=len(observer_target_dict[i])
			step+=1
		return total_count

	def demo(self):
		no_targets,no_observers,targets,observers=self.initialize()
		sorted_observers=sorted(observers,key=lambda x: x.limit)
		count_new=self.run(no_targets,no_observers,targets,sorted_observers)
		return count_new

	def test_run(self):
		for _ in range(30):
			for trgt in self.no_targets_arr:
				for obsver in self.no_observers_arr:
					for sns_rng_t in self.sensor_range:
						for sns_rng_o in self.sensor_range:
							(no_targets,no_observers,targets,observers)=self.initialize_param(trgt,obsver,sns_rng_t,sns_rng_o)
							print("No of Targets: ",trgt,"No of Observers: ",obsver,"Target's sensor range: ",sns_rng_t,"Observer's sensor range",sns_rng_o,main_orig(no_targets,no_observers,targets,observers))