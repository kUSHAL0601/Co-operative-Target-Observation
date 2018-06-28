import math
from random import random

class TargetsClass:
	def __init__(self,position_x,position_y,speed,angle,sensor_range):
		self.x=position_x
		self.y=position_y
		self.speed=speed
		self.angle=angle
		self.limit=sensor_range

	def update(self,x_limit,y_limit):
		temp_x=self.x+self.speed*math.cos(self.angle)
		temp_y=self.y+self.speed*math.sin(self.angle)
		if(temp_x>x_limit or temp_x<-x_limit):
			self.speed*=-1
		if(temp_y>y_limit or temp_y<-y_limit):
			self.speed*=-1
		temp_x=self.x+self.speed*math.cos(self.angle)
		temp_y=self.y+self.speed*math.sin(self.angle)
		self.x=temp_x
		self.y=temp_y

	def update_target(self,x_limit,y_limit,mean_x,mean_y):
		temp_x=mean_x
		temp_y=mean_y
		if(temp_x>x_limit or temp_x<-x_limit):
			temp_x=self.x+(random()*(x_limit/2)-(x_limit/4))
		if(temp_y>y_limit or temp_y<-y_limit):
			temp_y=self.y+(random()*(x_limit/2)-(x_limit/4))
		temp_x=0.7*temp_x + 0.3*(self.x+(random()*(x_limit/2)-(x_limit/4)))
		temp_y=0.7*temp_x + 0.3*(self.y+(random()*(y_limit/2)-(y_limit/4)))
		self.target_x=temp_x
		self.target_y=temp_y
		self.angle=-math.atan((temp_y-self.y)/(temp_x-self.x))

	def update_target_obst(self,x_limit,y_limit,mean_x,mean_y):
		temp_x=mean_x
		temp_y=mean_y
		# if(temp_x>x_limit or temp_x<-x_limit):
		# 	temp_x=self.x+(random()*(x_limit/2)-(x_limit/4))
		# if(temp_y>y_limit or temp_y<-y_limit):
		# 	temp_y=self.y+(random()*(x_limit/2)-(x_limit/4))
		# temp_x=0.7*temp_x + 0.3*(self.x+(random()*(x_limit/2)-(x_limit/4)))
		# temp_y=0.7*temp_x + 0.3*(self.y+(random()*(y_limit/2)-(y_limit/4)))
		self.target_x=temp_x
		self.target_y=temp_y
		self.angle=math.atan((temp_y-self.y)/(temp_x-self.x))

	def predict(self,x_limit,y_limit):
		temp_x=self.x+self.speed*math.cos(self.angle)
		temp_y=self.y+self.speed*math.sin(self.angle)
		if(temp_x>x_limit or temp_x<-x_limit):
			temp_x=self.x+(random()*(x_limit/2)-(x_limit/4))
		if(temp_y>y_limit or temp_y<-y_limit):
			temp_y=self.y+(random()*(x_limit/2)-(x_limit/4))
		return (temp_x,temp_y)

	def observer_in_range(self,observer):
		if(math.sqrt(pow(observer.x-self.x,2)+pow(observer.y-self.y,2))<=self.limit):
			return True
		else:
			return False

	def obstacle_in_range(self,obstacle_part):
		if(math.sqrt(pow(obstacle_part.x-self.x,2)+pow(obstacle_part.y-self.y,2))<=self.limit):
			return True
		else:
			return False
