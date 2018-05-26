from TargetsClass import TargetsClass as T
from ObserverClass import ObserverClass as O
from random import random

def reward(observer,targets,targets_to_consider,x_limit,y_limit,explore,mean_x,mean_y):
	rewards=[]
	for alphas in range(1,11):
		reward=0
		alpha=0.1*alphas
		temp_x=observer.x*(1-alpha)+alpha*explore*(random()*(x_limit/2)-(x_limit/4))+alpha*(1-explore)*mean_x
		temp_y=observer.y*(1-alpha)+alpha*explore*(random()*(y_limit/2)-(y_limit/4))+alpha*(1-explore)*mean_y
		for i in targets_to_consider:
			(predict_x,predict_y)=targets[i].predict(x_limit,y_limit)
			temp_enemy=T(predict_x,predict_y,0,0)
			if(observer.enemy_in_range(temp_enemy)):
				reward+=1
		rewards.append(reward)
	return rewards
