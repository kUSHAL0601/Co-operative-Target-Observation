import strat3
import strat4

from strat1 import strat1
from strat2 import strat2
from strat3 import strat3
from strat4 import strat4
from random import randint as RI
from random import random as R
from math import ceil,sin,cos
from copy import deepcopy
from ObserverClass import ObserverClass as O
from TargetsClass import TargetsClass as T
from ObstacleClass import ObstacleClass as Ob

def opp(l1x,l1y,l2x,l2y,p1x,p1y,p2x,p2y):
	'''
	p1,p2 are on opposite sides of line defined by l1,l2
	'''
	return ((l1y-l2y)*(p1x-l1x)+(l2x-l1x)*(p1y-l1y))*((l1y-l2y)*(p2x-l1x)+(l2x-l1x)*(p2y-l1y))<0

def between(ox,oy,tx,ty,l1x,l1y,l2x,l2y):
	'''
	ox,oy are observers co-ordinates
	tx,ty are targets coordinates
	l1x,l1y,l2x,l2y are end points of obstacles
	bx,by is any point between them
	'''
	bx=(l1x+l2x)/2
	by=(l1y+l2y)/2
	return ((l1y-oy)*(tx-l1x)+(ox-l1x)*(ty-l1y))*((l1y-oy)*(bx-l1x)+(ox-l1x)*(by-l1y))>=0 and ((l2y-oy)*(tx-l2x)+(ox-l2x)*(ty-l2y))*((l2y-oy)*(bx-l2x)+(ox-l2x)*(by-l2y))>=0


def mean(arr):
	n=len(arr)
	return sum(arr)/len(arr)


class hetero_main:
	def initialize(self):
		no_observers_arr=[2,6,10,14,18]
		no_targets_arr=[3,9,15,21,27]
		self.x_limit=150
		self.y_limit=150
		target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
		observer_speed=1.0
		sensor_range=[5,10,15,20,25]
		self.total_steps=1500
		self.update_steps=10
		observer_target_dict={}
		obstacle_len=[2,5,8,10,12,20]
		self.template_probability_distribution=[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5]
		targets=[]
		a=[-1 ,1]
		observers=[]
		obstacles=[]
		observer_strategy=[]
		no_targets=no_targets_arr[RI(0,4)]
		no_observers=no_observers_arr[RI(0,4)]
		no_obstacles=int(ceil(no_targets/3))
		for i in range(no_targets):
			targets.append(T(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],target_speed[RI(0,5)],R()*360,sensor_range[RI(0,4)]))
		for i in range(no_observers):
			observers.append(O(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],observer_speed,sensor_range[RI(0,4)]))
			observer_strategy.append(RI(3,4))
		for i in range(no_obstacles):
			obs_len=obstacle_len[RI(0,5)]
			angle=R()*360
			pos_x=R()*150*a[RI(0,1)]
			pos_y=R()*150*a[RI(0,1)]
			temp_obs=[]
			for j in range(obs_len):
				temp_obs.append(Ob(pos_x+j*sin(angle),pos_y+j*cos(angle),angle,i))
			obstacles.append((obs_len,temp_obs))
		return (no_targets,no_observers,no_obstacles,targets,observers,obstacles,observer_strategy)

	def initialize_custom(self,no_trgts,no_obs,obs_range):
		self.x_limit=150
		self.y_limit=150
		target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
		observer_speed=1.0
		self.total_steps=1500
		self.update_steps=10
		observer_target_dict={}
		obstacle_len=[2,5,8,10,12,20]
		self.template_probability_distribution=[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5]
		targets=[]
		a=[-1 ,1]
		observers=[]
		obstacles=[]
		observer_strategy=[]
		no_obstacles=int(ceil(no_trgts/3))
		sensor_range=[5,10,15,20,25]
		for i in range(no_trgts):
			targets.append(T(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],target_speed[RI(0,5)],R()*360,sensor_range[RI(0,4)]))
		for i in range(no_obs):
			observers.append(O(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],observer_speed,obs_range))
			observer_strategy.append(RI(3,4))
		for i in range(no_obstacles):
			obs_len=obstacle_len[RI(0,5)]
			angle=R()*360
			pos_x=R()*150*a[RI(0,1)]
			pos_y=R()*150*a[RI(0,1)]
			temp_obs=[]
			for j in range(obs_len):
				temp_obs.append(Ob(pos_x+j*sin(angle),pos_y+j*cos(angle),angle,i))
			obstacles.append((obs_len,temp_obs))
		return (no_trgts,no_obs,no_obstacles,targets,observers,obstacles,observer_strategy)

	def update_for_observers(self,observers,obstacles,targets):
		temp_dict={}
		temp_dict1={}
		for i in range(len(observers)):
			temp_dict[i]=[]
			temp_dict1[i]=[]
		for i in range(len(observers)):
			for j in range(len(obstacles)):
				for k in obstacles[j][1]:
					if(observers[i].obstacle_in_range(k)):
						temp_dict1[i].append(j)
						break
			for j in range(len(targets)):
				if(observers[i].enemy_in_range(targets[j])):
					for k in temp_dict1[i]:
						if opp(obstacles[k][1][0].x,obstacles[k][1][0].y,obstacles[k][1][obstacles[k][0]-1].x,obstacles[k][1][obstacles[k][0]-1].y,observers[i].x,observers[i].y,targets[j].x,targets[j].y) and (not between(observers[i].x,observers[i].y,targets[j].x,targets[j].y,obstacles[k][1][0].x,obstacles[k][1][0].y,obstacles[k][1][obstacles[k][0]-1].x,obstacles[k][1][obstacles[k][0]-1].y)):
							temp_dict[i].append(j)
		return [temp_dict,temp_dict1]

	def update_for_targets(self,observers,obstacles,targets):
		temp_dict={}
		temp_dict1={}
		for i in range(len(targets)):
			temp_dict[i]=[]
			temp_dict1[i]=[]
		for i in range(len(targets)):
			for j in range(len(observers)):
				if(targets[i].observer_in_range(observers[j])):
					temp_dict[i].append(j)
			for j in range(len(obstacles)):
				for k in obstacles[j][1]:
					if(targets[i].obstacle_in_range(k)):
						temp_dict1[i].append(j)
						break
		return [temp_dict,temp_dict1]

	def run(self,no_targets,no_observers,no_obstacles,targets,observers,obstacles,observer_strategy):
		step=0
		total_observed=0
		s1=strat1()
		s2=strat2()
		s3=strat3()
		s4=strat4()
		while(step<=self.total_steps):
			if(step%self.update_steps==0):
				for i in range(len(observers)):
					if observer_strategy[i]==1:
						s1.run_obs(no_targets,no_obstacles,targets,obstacles,observers[i])
					if observer_strategy[i]==2:
						s2.run_obs(no_targets,no_obstacles,targets,obstacles,observers[i])
					if observer_strategy[i]==3:
						s3.run_obs(no_targets,no_obstacles,targets,obstacles,observers[i])
					if observer_strategy[i]==4:
						s4.run_obs(no_targets,no_obstacles,targets,obstacles,observers[i])
				[target_observer_dict,target_obstacle_dict]=self.update_for_targets(observers,obstacles,targets)
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
			[observer_target_dict,observer_obstacle_dict]=self.update_for_observers(observers,obstacles,targets)
			for i in observer_target_dict:
				total_observed+=len(observer_target_dict[i])
			step+=1
		print("Heterogeneous strategy: ",total_observed)
		return total_observed

	def cmp(self):
		(no_targets,no_observers,no_obstacles,targets,observers,obstacles,observer_strategy)=self.initialize()
		t1=deepcopy(targets)
		t2=deepcopy(targets)
		t3=deepcopy(targets)
		t4=deepcopy(targets)
		o1=deepcopy(observers)
		o2=deepcopy(observers)
		o3=deepcopy(observers)
		o4=deepcopy(observers)
		ob1=deepcopy(obstacles)
		ob2=deepcopy(obstacles)
		ob3=deepcopy(obstacles)
		ob4=deepcopy(obstacles)
		tc=self.run(no_targets,no_observers,no_obstacles,targets,observers,obstacles,observer_strategy)
		strategy1=strat1()
		c1=strategy1.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		strategy2=strat2()
		c2=strategy2.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		strategy3=strat3()
		c3=strategy3.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		strategy4=strat4()
		c4=strategy4.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		return [tc,c1,c2,c3,c4]
	
	def custom_cmp(self,no_trgts,no_obs,obs_range):
		(no_targets,no_observers,no_obstacles,targets,observers,obstacles,observer_strategy)=self.initialize_custom(no_trgts,no_obs,obs_range)
		t1=deepcopy(targets)
		t2=deepcopy(targets)
		t3=deepcopy(targets)
		t4=deepcopy(targets)
		o1=deepcopy(observers)
		o2=deepcopy(observers)
		o3=deepcopy(observers)
		o4=deepcopy(observers)
		ob1=deepcopy(obstacles)
		ob2=deepcopy(obstacles)
		ob3=deepcopy(obstacles)
		ob4=deepcopy(obstacles)
		tc=self.run(no_targets,no_observers,no_obstacles,targets,observers,obstacles,observer_strategy)
		strategy1=strat1()
		c1=strategy1.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		strategy2=strat2()
		c2=strategy2.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		strategy3=strat3()
		c3=strategy3.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		strategy4=strat4()
		c4=strategy4.run(no_targets,no_observers,no_obstacles,t1,o1,ob1)
		return [tc,c1,c2,c3,c4]