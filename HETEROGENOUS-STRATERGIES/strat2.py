from ObserverClass import ObserverClass as O
from TargetsClass import TargetsClass as T
from ObstacleClass import ObstacleClass as Ob
from random import randint as RI
from random import random as R
from LP_CTO import LP_CTO
from BRLP_CTO import BRLP_CTO
from reward_obs_1 import reward_obs_1 as reward
from math import ceil,sin,cos

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

class strat2:
    def initialize(self):
        no_observers_arr=[2,6,10,14,18]
        no_targets_arr=[3,9,15,21,27]
        target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
        observer_speed=1.0
        sensor_range=[5,10,15,20,25]
        observer_target_dict={}
        obstacle_len=[2,5,8,10,12,20]
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

    def run(self,no_targets,no_observers,no_obstacles,targets,observers,obstacles):
        total_observed=0
        step=0
        data_until_update=[]
        while(step<=1500):
            if(step%10==0):
                [observer_target_dict,observer_obstacle_dict]=self.update_for_observers(observers,obstacles,targets)
                [target_observer_dict,target_obstacle_dict]=self.update_for_targets(observers,obstacles,targets)
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
                        rwrd=reward(observers[i],targets,observer_target_dict[i],obstacles,observer_obstacle_dict[i],150,150,explore,mean_x,mean_y)
                        E_min=LP_CTO(rwrd,1.0,[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5])[0]
                        alpha=BRLP_CTO(rwrd,[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5],E_min)
                        observers[i].update_target(alpha,explore,150,150,mean_x,mean_y)
                        if(len(observer_obstacle_dict[i])):
                            observers[i].sleep=True
                    else:
                        observers[i].update_target(1,1,150,150,0,0)

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
                        targets[i].update_target(150,150,mean_x,mean_y)
                    elif(len(target_obstacle_dict[i])):
                        obst_idx=target_obstacle_dict[i][0]
                        sx=0
                        sy=0
                        for j in obstacles[obst_idx][1]:
                            sx+=j.x
                            sy+=j.y
                        n=obstacles[obst_idx][0]
                        # print("Found obstacle at ",sx/n,sy/n)
                        targets[i].update_target_obst(150,150,sx/n,sy/n)

            for i in observers:
                i.update(150,150)
            for i in targets:
                i.update(150,150)
            step+=1
            [observer_target_dict,observer_obstacle_dict]=self.update_for_observers(observers,obstacles,targets)
            for i in observer_target_dict:
                total_observed+=len(observer_target_dict[i])
        print("Stratergy 2: ",total_observed)
        return total_observed

    def run_obs(self,no_targets,no_obstacles,targets,obstacles,observer_object):
        total_observed=0
        step=0
        data_until_update=[]
        [observer_target_dict,observer_obstacle_dict]=self.update_for_observers([observer_object],obstacles,targets)
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
                rwrd=reward(observer_object,targets,observer_target_dict[i],obstacles,observer_obstacle_dict[i],150,150,explore,mean_x,mean_y)
                E_min=LP_CTO(rwrd,1.0,[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5])[0]
                alpha=BRLP_CTO(rwrd,[0.001953125, 0.001953125, 0.00390625, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125,0.25,0.5],E_min)
                observer_object.update_target(alpha,explore,150,150,mean_x,mean_y)
                if(len(observer_obstacle_dict[i])):
                    observer_object.sleep=True
            else:
                observer_object.update_target(1,1,150,150,0,0)

        for i in observer_target_dict:
            total_observed+=len(observer_target_dict[i])
        if total_observed>0:
            print("Observer using Stratergy 2: ",total_observed)
        return total_observed


    def run_default(self):
        (no_targets,no_observers,no_obstacles,targets,observers,obstacles)=self.initialize()
        tc=self.run(no_targets,no_observers,no_obstacles,targets,observers,obstacles)
        # for i in range(15000):
        #     if i%10==0:
        #         tc=self.run_obs(no_targets,no_obstacles,targets,obstacles,observers[0])
        #     observers[0].update(150,150)        