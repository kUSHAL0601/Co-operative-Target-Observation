import math
from random import random

class ObserverClass:
	def __init__(self,position_x,position_y,speed,sensor_range):
		self.x=position_x
		self.y=position_y
		self.speed=speed
		self.limit=sensor_range

	def update_target(self,alpha,explore,x_limit,y_limit,mean_x,mean_y):
		temp_x=self.x*(1-alpha)+alpha*explore*(random()*(x_limit/2)-(x_limit/4))+alpha*(1-explore)*mean_x
		temp_y=self.y*(1-alpha)+alpha*explore*(random()*(y_limit/2)-(y_limit/4))+alpha*(1-explore)*mean_y
		if(temp_x>x_limit or temp_x<-x_limit):
			temp_x=random()*(x_limit/2)-(x_limit/4)
		if(temp_y>y_limit or temp_y<-y_limit):
			temp_y=random()*(x_limit/2)-(x_limit/4)
		self.target_x=temp_x
		self.target_y=temp_y
		self.angle=math.atan((temp_y-self.y)/(temp_x-self.x))

	def update(self,x_limit,y_limit):
		temp_x=self.x+self.speed*math.cos(self.angle)
		temp_y=self.y+self.speed*math.sin(self.angle)
		if(temp_x>x_limit or temp_x<-x_limit):
			temp_x=random()*(x_limit/2)-(x_limit/4)
		if(temp_y>y_limit or temp_y<-y_limit):
			temp_y=random()*(x_limit/2)-(x_limit/4)
		self.x=temp_x
		self.y=temp_y

	def enemy_in_range(self,enemy):
		if(math.sqrt(pow(enemy.x-self.x,2)+pow(enemy.y-self.y,2))<=self.limit):
			return True
		else:
			return False
