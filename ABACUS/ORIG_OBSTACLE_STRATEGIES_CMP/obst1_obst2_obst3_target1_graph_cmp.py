from ObserverClass import ObserverClass as O
from TargetsClass import TargetsClass as T
from ObstacleClass import ObstacleClass as Ob
from random import randint as RI
from random import random as R
from LP_CTO import LP_CTO
from BRLP_CTO import BRLP_CTO
from reward import reward
from reward_obs_1 import reward_obs_1
from math import ceil,sin,cos
import math
from copy import deepcopy
from arc_tan import arc_tan as tan_inv
import matplotlib.pyplot as plt

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
	if(n==0):
		return 0
	return sum(arr)/n

# no_observers_arr=[2,6,10,14,18]
# no_targets_arr=[3,9,15,21,27]
no_observers_arr=[2,5,10,14,18,20,50]
# no_observers_arr=[2,5]
no_targets_arr=[3,9,15,21,27,50,100]
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
obstacle_len=[2,5,8,10,12,20]
graph_colors=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
#for i in range(10):
#	template_probability_distribution.append(0.1)
template_probability_distribution=[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5]


def initialize():
	targets=[]
	a=[-1 ,1]
	observers=[]
	obstacles=[]
	no_targets=no_targets_arr[RI(0,4)]
	no_observers=no_observers_arr[RI(0,4)]
	no_obstacles=int(ceil(no_targets/3))
	for i in range(no_targets):
		targets.append(T(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],target_speed[RI(0,5)],R()*360,sensor_range[RI(0,4)]))
	for i in range(no_observers):
		observers.append(O(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],observer_speed,sensor_range[RI(0,4)]))
	for i in range(no_obstacles):
		obs_len=obstacle_len[RI(0,5)]
		angle=R()*360
		pos_x=R()*150*a[RI(0,1)]
		pos_y=R()*150*a[RI(0,1)]
		temp_obs=[]
		for j in range(obs_len):
			temp_obs.append(Ob(pos_x+j*sin(angle),pos_y+j*cos(angle),angle,i))
		obstacles.append((obs_len,temp_obs))
	return (no_targets,no_observers,no_obstacles,targets,observers,obstacles)

def initialize_param(no_targets,no_observers,spd):
	targets=[]
	a=[-1 ,1]
	observers=[]
	obstacles=[]
	no_obstacles=int(ceil(no_targets/3))
	for i in range(no_targets):
		targets.append(T(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],spd,R()*360,sensor_range[RI(0,4)]))
	for i in range(no_observers):
		observers.append(O(R()*150*a[RI(0,1)],R()*150*a[RI(0,1)],observer_speed,sensor_range[RI(0,4)]))
	for i in range(no_obstacles):
		obs_len=obstacle_len[RI(0,5)]
		angle=R()*360
		pos_x=R()*150*a[RI(0,1)]
		pos_y=R()*150*a[RI(0,1)]
		temp_obs=[]
		for j in range(obs_len):
			temp_obs.append(Ob(pos_x+j*sin(angle),pos_y+j*cos(angle),angle,i))
		obstacles.append((obs_len,temp_obs))
	return (no_targets,no_observers,no_obstacles,targets,observers,obstacles)

def update_for_observers(observers,targets,obstacles):
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

def update_for_targets(observers,targets,obstacles):
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

def main_obstacle_1(no_targets,no_observers,no_obstacles,targets,observers,obstacles):
	step=0
	data_until_update=[]
	total_count_obst=0
	while(step<=total_steps):
		if(step%update_steps==0):
			[observer_target_dict,observer_obstacle_dict]=update_for_observers(observers,targets,obstacles)
			[target_observer_dict,target_obstacle_dict]=update_for_targets(observers,targets,obstacles)
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
					rwrd=reward_obs_1(observers[i],targets,observer_target_dict[i],obstacles,observer_obstacle_dict[i],x_limit,y_limit,explore,mean_x,mean_y)
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
				target_obstacle_dict[i].sort(reverse=True,key=lambda i: obstacles[i][0])
				if(len(temp_arr_x) and len(temp_arr_y)):
					mean_x=mean(temp_arr_x)
					mean_y=mean(temp_arr_y)
					obst_idx=-1
					tan_inv_ot=tan_inv((targets[i].y-mean_y),(targets[i].x-mean_x))
					for j in target_obstacle_dict[i]:
						tan_inv_oo=tan_inv((obstacles[j][1][0].y-mean_y),(obstacles[j][1][0].x-mean_x))
						if(abs(tan_inv_oo - tan_inv_ot)<=math.pi/2):
							obst_idx=j
							break
					if(obst_idx==-1):
						targets[i].update_target(x_limit,y_limit,mean_x,mean_y)
					else:
						sx=0
						sy=0
						for j in obstacles[obst_idx][1]:
							sx+=j.x
							sy+=j.y
						n=obstacles[obst_idx][0]
						targets[i].update_target_obst(x_limit,y_limit,sx/n,sy/n)

		for i in observers:
			i.update(x_limit,y_limit)
		for i in targets:
			i.update(x_limit,y_limit)
		step+=1
		ans_dict=update_for_observers1(observers,targets)
		for i in ans_dict:
			for j in ans_dict[i]:
				total_count_obst+=1
	return total_count_obst


#OBSTACLE 2

def update_for_observers1(observers,targets):
	temp_dict={}
	for i in range(len(observers)):
		temp_dict[i]=[]
	for i in range(len(observers)):
		for j in range(len(targets)):
			if(observers[i].enemy_in_range(targets[j])):
				temp_dict[i].append(j)
	return temp_dict

def update_for_targets1(observers,targets):
	temp_dict={}
	for i in range(len(targets)):
		temp_dict[i]=[]
	for i in range(len(targets)):
		for j in range(len(observers)):
			if(targets[i].observer_in_range(observers[j])):
				temp_dict[i].append(j)
	return temp_dict

def main_obstacle_2(no_targets,no_observers,no_obstacles,targets,observers,obstacles):
	step=0
	data_until_update=[]
	total_count_obst=0
	while(step<=total_steps):
		if(step%update_steps==0):
			[observer_target_dict,observer_obstacle_dict]=update_for_observers(observers,targets,obstacles)
			[target_observer_dict,target_obstacle_dict]=update_for_targets(observers,targets,obstacles)
			for i in observer_target_dict:
				temp_arr_x=[]
				temp_arr_y=[]
				obs_arr_x=[]
				obs_arr_y=[]
				for j in observer_target_dict[i]:
					temp_arr_x.append(targets[j].x)
					temp_arr_y.append(targets[j].y)
				for j in observer_obstacle_dict[i]:
					for k in obstacles[j][1]:
						obs_arr_x.append(k.x)
						obs_arr_y.append(k.y)
				if(len(temp_arr_x)):
					if(len(obs_arr_x)):
						mean_x=mean(temp_arr_x)*0.9+mean(obs_arr_x)*0.1
						mean_y=mean(temp_arr_y)*0.9+mean(obs_arr_y)*0.1
					else:
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
				target_obstacle_dict[i].sort(reverse=True,key=lambda i: obstacles[i][0])
				if(len(temp_arr_x) and len(temp_arr_y)):
					mean_x=mean(temp_arr_x)
					mean_y=mean(temp_arr_y)
					obst_idx=-1
					tan_inv_ot=tan_inv((targets[i].y-mean_y),(targets[i].x-mean_x))
					for j in target_obstacle_dict[i]:
						tan_inv_oo=tan_inv((obstacles[j][1][0].y-mean_y),(obstacles[j][1][0].x-mean_x))
						if(abs(tan_inv_oo - tan_inv_ot)<=math.pi/2):
							obst_idx=j
							break
					if(obst_idx==-1):
						targets[i].update_target(x_limit,y_limit,mean_x,mean_y)
					else:
						sx=0
						sy=0
						for j in obstacles[obst_idx][1]:
							sx+=j.x
							sy+=j.y
						n=obstacles[obst_idx][0]
						targets[i].update_target_obst(x_limit,y_limit,sx/n,sy/n)

		for i in observers:
			i.update(x_limit,y_limit)
		for i in targets:
			i.update(x_limit,y_limit)
		step+=1
		ans_dict=update_for_observers1(observers,targets)
		for i in ans_dict:
			for j in ans_dict[i]:
				total_count_obst+=1
	return total_count_obst

# OBSTACLE 2 END

# OBSTACLE 3 START

def main_obstacle_3(no_targets,no_observers,no_obstacles,targets,observers,obstacles):
	step=0
	data_until_update=[]
	total_count_obst=0
	while(step<=total_steps):
		if(step%update_steps==0):
			[observer_target_dict,observer_obstacle_dict]=update_for_observers(observers,targets,obstacles)
			[target_observer_dict,target_obstacle_dict]=update_for_targets(observers,targets,obstacles)
			for i in observer_target_dict:
				temp_arr_x=[]
				temp_arr_y=[]
				obs_arr_x=[]
				obs_arr_y=[]
				for j in observer_target_dict[i]:
					temp_arr_x.append(targets[j].x)
					temp_arr_y.append(targets[j].y)
				for j in observer_obstacle_dict[i]:
					for k in obstacles[j][1]:
						obs_arr_x.append(k.x)
						obs_arr_y.append(k.y)
				if(len(temp_arr_x)):
					mean_x=mean(temp_arr_x)
					mean_y=mean(temp_arr_y)
					explore=pow(1/(len(observer_target_dict[i])+1),2)
					rwrd=reward(observers[i],targets,observer_target_dict[i],x_limit,y_limit,explore,mean_x,mean_y)
					E_min=LP_CTO(rwrd,1.0,template_probability_distribution)[0]
					alpha=BRLP_CTO(rwrd,template_probability_distribution,E_min)
					observers[i].update_target(alpha,explore,x_limit,y_limit,mean_x,mean_y)
				else:
					if(len(obs_arr_x)):
						mean_x=mean(obs_arr_x)
						mean_y=mean(obs_arr_y)
						explore=pow(1/(len(obs_arr_x)+1),2)
						observers[i].update_target(1,explore,x_limit,y_limit,mean_x,mean_y)
					else:
						observers[i].update_target(1,1,x_limit,y_limit,0,0)

			for i in target_observer_dict:
				temp_arr_x=[]
				temp_arr_y=[]
				for j in target_observer_dict[i]:
					temp_arr_x.append(observers[j].x)
					temp_arr_y.append(observers[j].y)
				target_obstacle_dict[i].sort(reverse=True,key=lambda i: obstacles[i][0])
				if(len(temp_arr_x) and len(temp_arr_y)):
					mean_x=mean(temp_arr_x)
					mean_y=mean(temp_arr_y)
					obst_idx=-1
					tan_inv_ot=tan_inv((targets[i].y-mean_y),(targets[i].x-mean_x))
					for j in target_obstacle_dict[i]:
						tan_inv_oo=tan_inv((obstacles[j][1][0].y-mean_y),(obstacles[j][1][0].x-mean_x))
						if(abs(tan_inv_oo - tan_inv_ot)<=math.pi/2):
							obst_idx=j
							break
					if(obst_idx==-1):
						targets[i].update_target(x_limit,y_limit,mean_x,mean_y)
					else:
						sx=0
						sy=0
						for j in obstacles[obst_idx][1]:
							sx+=j.x
							sy+=j.y
						n=obstacles[obst_idx][0]
						targets[i].update_target_obst(x_limit,y_limit,sx/n,sy/n)

		for i in observers:
			i.update(x_limit,y_limit)
		for i in targets:
			i.update(x_limit,y_limit)
		step+=1
		ans_dict=update_for_observers1(observers,targets)
		for i in ans_dict:
			for j in ans_dict[i]:
				total_count_obst+=1
	return total_count_obst


# OBSTACLE 3 END

# MAIN START

def main_orig(no_targets,no_observers,targets,observers):
	step=0
	data_until_update=[]
	total_count=0
	while(step<=total_steps):
		if(step%update_steps==0):
			observer_target_dict=update_for_observers1(observers,targets)
			target_observer_dict=update_for_targets1(observers,targets)
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
		step+=1
		ans_dict=update_for_observers1(observers,targets)
		for i in ans_dict:
			for j in ans_dict[i]:
				total_count+=1
	return total_count			


# MAIN END


d12={}
d21={}
d13={}
d31={}
d23={}
d32={}
for k in range(30):
	for i in no_observers_arr:
		for j in no_targets_arr:
			for l in target_speed:
				no_targets,no_observers,no_obstacles,targets,observers,obstacles=initialize_param(j,i,l)
				targets1=deepcopy(targets)
				observers1=deepcopy(observers)
				obstacles1=deepcopy(obstacles)
				targets2=deepcopy(targets)
				observers2=deepcopy(observers)
				obstacles2=deepcopy(obstacles)

				targets3=deepcopy(targets)
				observers3=deepcopy(observers)

				mo1=main_obstacle_1(no_targets,no_observers,no_obstacles,targets,observers,obstacles)
				mo2=main_obstacle_2(no_targets,no_observers,no_obstacles,targets1,observers1,obstacles1)
				mo3=main_obstacle_3(no_targets,no_observers,no_obstacles,targets2,observers2,obstacles2)
				m=main_orig(no_targets,no_observers,targets3,observers3)
				if((j,l) in d12):
					if(mo1):
						d12[(j,l)].append((m-mo1)/mo1)
					if(mo2):
						d21[(j,l)].append((m-mo2)/mo2)
					if(mo3):
						d31[(j,l)].append((m-mo3)/mo3)
					if(m):
						d13[(j,l)].append((mo1-m)/m)
						d23[(j,l)].append((mo2-m)/m)
						d32[(j,l)].append((mo3-m)/m)
				else:
					if(mo1):
						d12[(j,l)]=[(m-mo1)/mo1]
					else:
						d12[(j,l)]=[]
					if(mo2):
						d21[(j,l)]=[(m-mo2)/mo2]
					else:
						d21[(j,l)]=[]
					if(mo3):
						d31[(j,l)]=[(m-mo3)/mo3]
					else:
						d31[(j,l)]=[]
					if(m):
						d13[(j,l)]=[(mo1-m)/m]
						d23[(j,l)]=[(mo2-m)/m]
						d32[(j,l)]=[(mo3-m)/m]
					else:
						d13[(j,l)]=[]
						d23[(j,l)]=[]
						d32[(j,l)]=[]

for i in d12:
	d12[i]=mean(d12[i])
for i in d21:
	d21[i]=mean(d21[i])
for i in d13:
	d13[i]=mean(d13[i])
for i in d31:
	d31[i]=mean(d31[i])
for i in d23:
	d23[i]=mean(d23[i])
for i in d32:
	d32[i]=mean(d32[i])
# print(d12,d21,)
x_axis=deepcopy(no_targets_arr)
for i in range(len(target_speed)):
	y_axis_12=[]
	y_axis_21=[]
	y_axis_13=[]
	y_axis_31=[]
	y_axis_23=[]
	y_axis_32=[]
	for j in x_axis:
		y_axis_12.append(d12[(j,target_speed[i])])
		y_axis_21.append(d21[(j,target_speed[i])])
		y_axis_13.append(d13[(j,target_speed[i])])
		y_axis_31.append(d31[(j,target_speed[i])])
		y_axis_23.append(d23[(j,target_speed[i])])
		y_axis_32.append(d32[(j,target_speed[i])])
	plt.figure(1)
	plt.plot(x_axis,y_axis_12,color=graph_colors[i],label="Speed: "+str(target_speed[i]))
	plt.figure(2)
	plt.plot(x_axis,y_axis_21,color=graph_colors[i],label="Speed: "+str(target_speed[i]))
	plt.figure(3)
	plt.plot(x_axis,y_axis_13,color=graph_colors[i],label="Speed: "+str(target_speed[i]))
	plt.figure(4)
	plt.plot(x_axis,y_axis_31,color=graph_colors[i],label="Speed: "+str(target_speed[i]))
	plt.figure(5)
	plt.plot(x_axis,y_axis_23,color=graph_colors[i],label="Speed: "+str(target_speed[i]))
	plt.figure(6)
	plt.plot(x_axis,y_axis_32,color=graph_colors[i],label="Speed: "+str(target_speed[i]))

plt.figure(1)
plt.xlabel("No. of targets")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy 1 to Original")

plt.figure(2)
plt.xlabel("No. of targets")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy 2 to Original")

plt.figure(3)
plt.xlabel("No. of targets")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy Original to 1")

plt.figure(4)
plt.xlabel("No. of targets")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy 3 to Original")

plt.figure(5)
plt.xlabel("No. of targets")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy Original to 2")

plt.figure(6)
plt.xlabel("No. of targets")
plt.ylabel("Mean diffrence between strategies")
plt.legend()
plt.title("Comparing strategy Original to 3")

plt.figure(1)
plt.savefig("Obst1-Orig.png")
plt.figure(2)
plt.savefig("Obst2-Orig.png")

plt.figure(3)
plt.savefig("Orig-Obst1.png")
plt.figure(4)
plt.savefig("Obst3-Orig.png")

plt.figure(5)
plt.savefig("Orig-Obst2.png")
plt.figure(6)
plt.savefig("Orig-Obst3.png")
