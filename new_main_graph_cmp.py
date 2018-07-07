from ObserverClass import ObserverClass as O
from TargetsClass import TargetsClass as T
from random import randint as RI
from random import random as R
from LP_CTO import LP_CTO
from BRLP_CTO import BRLP_CTO
from reward import reward
from copy import deepcopy
from matplotlib import pyplot as plt

def mean(arr):
	n=len(arr)
	return sum(arr)/len(arr)

no_observers_arr=[2,6,10,14,18,20,50,100,150,200]
# no_observers_arr=[2,6]
no_targets_arr=[3,9,15,21,27,50]
# no_targets_arr=[3,9]
x_limit=150
y_limit=150
target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
# target_speed=[0.2,0.5]
observer_speed=1.0
sensor_range=[5,10,15,20,25]
total_steps=1500
update_steps=10
observer_target_dict={}
template_probability_distribution=[]
#for i in range(10):
#	template_probability_distribution.append(0.1)
template_probability_distribution=[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5]
graph_colors=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


def initialize():
	targets=[]
	observers=[]
	no_targets=no_targets_arr[RI(0,4)]
	no_observers=no_observers_arr[RI(0,4)]
	for i in range(no_targets):
		targets.append(T(R()*150,R()*150,target_speed[RI(0,5)],R()*360,sensor_range[RI(0,4)]))
	for i in range(no_observers):
		observers.append(O(R()*150,R()*150,observer_speed,sensor_range[RI(0,4)]))
	return (no_targets,no_observers,targets,observers)

def initialize_param(no_targets,no_observers,t_spd):
	targets=[]
	observers=[]
	for i in range(no_targets):
		targets.append(T(R()*150,R()*150,t_spd,R()*360,sensor_range[RI(0,4)]))
	for i in range(no_observers):
		observers.append(O(R()*150,R()*150,observer_speed,sensor_range[RI(0,4)]))
	return (no_targets,no_observers,targets,observers)

def update_for_observers(observers,targets):
	temp_dict={}
	for i in range(len(observers)):
		temp_dict[i]=[]
	for i in range(len(observers)):
		for j in range(len(targets)):
			if(observers[i].enemy_in_range(targets[j])):
				temp_dict[i].append(j)
	return temp_dict

def update_for_targets(observers,targets):
	temp_dict={}
	for i in range(len(targets)):
		temp_dict[i]=[]
	for i in range(len(targets)):
		for j in range(len(observers)):
			if(targets[i].observer_in_range(observers[j])):
				temp_dict[i].append(j)
	return temp_dict

def main_orig(no_targets,no_observers,targets,observers):
	step=0
	count=0
	data_until_update=[]
	while(step<=total_steps):
		if(step%update_steps==0):
			observer_target_dict=update_for_observers(observers,targets)
			target_observer_dict=update_for_targets(observers,targets)
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

			for i in target_observer_dict:
				temp_arr_x=[]
				temp_arr_y=[]
				for j in target_observer_dict[i]:
					temp_arr_x.append(observers[j].x)
					temp_arr_y.append(observers[j].y)
				if(len(temp_arr_x) and len(temp_arr_y)):
					mean_x=mean(temp_arr_x)
					mean_y=mean(temp_arr_y)
					targets[i].update_target(x_limit,y_limit,mean_x,mean_y)

		for i in observers:
			i.update(x_limit,y_limit)
		for i in targets:
			i.update(x_limit,y_limit)
		tmp_observer_target_dict=update_for_observers(observers,targets)
		tmp_arr=[]
		for i in tmp_observer_target_dict:
			for j in tmp_observer_target_dict[i]:
				if(j not in tmp_arr):
					tmp_arr.append(j)
		# print("Observers observed in "+str(step)+"is "+str(len(tmp_arr)))
		count+=len(tmp_arr)
		step+=1
	return count

def main_new(no_targets,no_observers,targets,observers,threshold):
	step=0
	count=0
	data_until_update=[]
	while(step<=total_steps):
		if(step%update_steps==0):
			observer_target_dict=update_for_observers(observers,targets)
			target_observer_dict=update_for_targets(observers,targets)
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
						observers[i].update_target(1,1,x_limit,y_limit,0,0)
						# print("Exploring")
					else:
						mean_x=mean(temp_arr_x)
						mean_y=mean(temp_arr_y)
						explore=pow(1/(len(observer_target_dict[i])+1),2)
						rwrd=reward(observers[i],targets,observer_target_dict[i],x_limit,y_limit,explore,mean_x,mean_y)
						E_min=LP_CTO(rwrd,1.0,template_probability_distribution)[0]
						alpha=BRLP_CTO(rwrd,template_probability_distribution,E_min)
						observers[i].update_target(alpha,explore,x_limit,y_limit,mean_x,mean_y)
						for j in observer_target_dict[i]:
							targets_included[j]=1
				else:
					observers[i].update_target(1,1,x_limit,y_limit,0,0)

			for i in target_observer_dict:
				temp_arr_x=[]
				temp_arr_y=[]
				for j in target_observer_dict[i]:
					temp_arr_x.append(observers[j].x)
					temp_arr_y.append(observers[j].y)
				if(len(temp_arr_x) and len(temp_arr_y)):
					mean_x=mean(temp_arr_x)
					mean_y=mean(temp_arr_y)
					targets[i].update_target(x_limit,y_limit,mean_x,mean_y)

		for i in observers:
			i.update(x_limit,y_limit)
		for i in targets:
			i.update(x_limit,y_limit)
		tmp_observer_target_dict=update_for_observers(observers,targets)
		tmp_arr=[]
		for i in tmp_observer_target_dict:
			for j in tmp_observer_target_dict[i]:
				if(j not in tmp_arr):
					tmp_arr.append(j)
		# print("Observers observed in "+str(step)+"is "+str(len(tmp_arr)))
		count+=len(tmp_arr)
		step+=1
	return count
d1={}
d2={}
for k in range(30):
	for i in no_observers_arr:
		for j in no_targets_arr:
			for l in target_speed:
				(no_targets,no_observers,targets,observers)=initialize_param(j,i,l)
				targets1=deepcopy(targets)
				targets2=deepcopy(targets)
				observers1=deepcopy(observers)
				count_orig=main_orig(no_targets,no_observers,targets1,observers1)
				sorted_observers=deepcopy(observers)
				sorted_observers=sorted(sorted_observers,key=lambda x: x.limit)
				count_new=main_new(no_targets,no_observers,targets2,sorted_observers,0.2)
				if (i/j,l) in d1:
					if(count_orig):
						d1[(i/j,l)].append((count_orig-count_new)/count_orig)
					if(count_new):
						d2[(i/j,l)].append((count_new-count_orig)/count_new)
				else:
					if(count_orig):
						d1[(i/j,l)]=[(count_orig-count_new)/count_orig]
					else:
						d1[(i/j,l)]=[]
					if(count_new):
						d2[(i/j,l)]=[(count_new-count_orig)/count_new]
					else:
						d2[(i/j,l)]=[]
for i in d1:
	d1[i]=mean(d1[i])
for i in d2:
	d2[i]=mean(d2[i])
x_axis_1=list(set([i[0] for i in d1]))
x_axis_2=list(set([i[0] for i in d2]))
for i in range(len(target_speed)):
	y_axis_1=[]
	y_axis_2=[]
	for j in x_axis_1:
		y_axis_1.append(d1[(j,target_speed[i])])
	for j in x_axis_2:
		y_axis_2.append(d2[(j,target_speed[i])])
	plt.figure(1)
	plt.plot(x_axis_1,y_axis_1,color=graph_colors[i],label="Speed: "+str(target_speed[i]))
	plt.figure(2)
	plt.plot(x_axis_2,y_axis_2,color=graph_colors[i],label="Speed: "+str(target_speed[i]))

plt.figure(1)
plt.xlabel("Observer/Target ratio")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy Non-Communicative to Communicative")

plt.figure(2)
plt.xlabel("Observer/Target ratio")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy Communicative to Non-Communicative")

plt.figure(1)
plt.savefig("Non-Communicative-vs-Communicative-20Thresh.png")

plt.figure(2)
plt.savefig("Communicative-vs-Non-Communicative-20Thresh.png")


# plt.show()

# print(x_axis)
