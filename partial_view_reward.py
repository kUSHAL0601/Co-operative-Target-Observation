from random import random
import math

def reward(observer,targets,targets_to_consider,x_limit,y_limit,explore,mean_x,mean_y):
	rewards=[]
	for alphas in range(1,11):
		reward=0
		alpha=0.1*alphas
		temp_x=observer.x*(1-alpha)+alpha*explore*(random()*(x_limit/2)-(x_limit/4))+alpha*(1-explore)*mean_x
		temp_y=observer.y*(1-alpha)+alpha*explore*(random()*(y_limit/2)-(y_limit/4))+alpha*(1-explore)*mean_y
		for i in targets_to_consider:
			(predict_x,predict_y)=targets[i].predict(x_limit,y_limit)
			dist_x=predict_x - temp_x
			dist_y=predict_y - temp_y
			if(math.sqrt(pow(dist_x,2)+pow(dist_y,2))<=observer.limit and dist_x>=0):
				reward+=1
		rewards.append(reward)
#	print(rewards)
	return rewards
