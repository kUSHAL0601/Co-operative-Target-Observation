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

no_observers_arr=[2,6,10,14,18]
no_targets_arr=[3,9,15,21,27]
x_limit=150
y_limit=150
target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
observer_speed=1.0
sensor_range=[5,10,15,20,25]
total_steps=1500
update_steps=10
observer_target_dict={}
template_probability_distribution=[]
#for i in range(10):
#	template_probability_distribution.append(0.1)
template_probability_distribution=[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5]

def initialize():
	targets=[]
	observers=[]
	no_targets=no_targets_arr[RI(0,4)]
	no_observers=no_observers_arr[RI(0,4)]
	for i in range(no_targets):
		targets.append(T(R()*150,R()*150,target_speed[RI(0,5)],R()*360))
	for i in range(no_observers):
		observers.append(O(R()*150,R()*150,observer_speed,sensor_range[RI(0,4)]))
	return (no_targets,no_observers,targets,observers)

def update():
	temp_dict={}
	for i in range(len(observers)):
		temp_dict[i]=[]
	for i in range(len(observers)):
		for j in range(len(targets)):
			if(observers[i].enemy_in_range(targets[j])):
				temp_dict[i].append(j)
	return temp_dict

def main_orig(no_targets,no_observers,targets,observers):
	step=0
	data_until_update=[]
	while(step<=total_steps):
		if(step%update_steps==0):
			observer_target_dict=update()
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
					rwrd=reward(observers[i],targets,observer_target_dict[i],x_limit,y_limit,explore,mean_x,mean_y)
					E_min=LP_CTO(rwrd,1.0,template_probability_distribution)[0]
					alpha=BRLP_CTO(rwrd,template_probability_distribution,E_min)
					observers[i].update_target(alpha,explore,x_limit,y_limit,mean_x,mean_y)
				else:
					observers[i].update_target(1,1,x_limit,y_limit,0,0)
		for i in observers:
			i.update(x_limit,y_limit)
		for i in targets:
			i.update(x_limit,y_limit)
		print(len(observers)+len(targets))
		print(step)
		for i in targets:
			print("H",float(i.x),float(i.y),0.0)
		for i in observers:
			print("N",float(i.x),float(i.y),0.0)
		step+=1

(no_targets,no_observers,targets,observers)=initialize()
main_orig(no_targets,no_observers,targets,observers)
