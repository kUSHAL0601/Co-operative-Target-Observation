import math
from random import random
from arc_tan import arc_tan as tan_inv

class ObserverClass:
	def __init__(self,position_x,position_y,speed,sensor_range):
		self.x=position_x
		self.y=position_y
		self.speed=speed
		self.limit=sensor_range
		self.obstacle=-1
		self.goAround=-1
		self.old_pos_x=0
		self.old_pos_y=0
		self.sleep=False
		self.angle=0

	def update_target(self,alpha,explore,x_limit,y_limit,mean_x,mean_y):
		if self.sleep:
			self.sleep=False
			return
		temp_x=self.x*(1-alpha)+alpha*explore*(self.x+(random()*(x_limit/2)-(x_limit/4)))+alpha*(1-explore)*mean_x
		temp_y=self.y*(1-alpha)+alpha*explore*(self.y+(random()*(y_limit/2)-(y_limit/4)))+alpha*(1-explore)*mean_y
		if(temp_x>x_limit or temp_x<-x_limit):
			while(not (temp_x>x_limit or temp_x<-x_limit)):
				temp_x=self.x+(random()*(x_limit/2)-(x_limit/4))
		if(temp_y>y_limit or temp_y<-y_limit):
			while(not (temp_y>y_limit or temp_y<-y_limit)):
				temp_y=self.y+(random()*(x_limit/2)-(x_limit/4))
		self.target_x=temp_x
		self.target_y=temp_y
		self.angle=tan_inv((temp_y-self.y),(temp_x-self.x))
		# print(self.angle)

	def update(self,x_limit,y_limit):
		if self.sleep:
			self.sleep=False
			return
		temp_x=self.x+self.speed*math.cos(self.angle)
		temp_y=self.y+self.speed*math.sin(self.angle)
		if(temp_x>x_limit):
			temp_x=x_limit
		if(temp_x<-x_limit):
			temp_x=-x_limit
		if(temp_y>y_limit):
			temp_y=y_limit
		if(temp_y<-y_limit):
			temp_y=-y_limit
		self.x=temp_x
		self.y=temp_y

	def enemy_in_range(self,enemy):
		if(math.sqrt(pow(enemy.x-self.x,2)+pow(enemy.y-self.y,2))<=self.limit):
			return True
		else:
			return False

	def obstacle_in_range(self,obstacle_part):
		if(math.sqrt(pow(obstacle_part.x-self.x,2)+pow(obstacle_part.y-self.y,2))<=self.limit):
			return True
		else:
			return False

	def update_goAround(obstacle):
		if(self.goAround==1):
			self.x+=sin(tan_inv(obstacle.y-self.y/obstacle.x-self.x))
			self.y+=cos(tan_inv(obstacle.y-self.y/obstacle.x-self.x))
			if((pow(abs(self.x-obstacle.x),2)+pow(abs(self.y-obstacle.y),2))>=100):
				self.goAround=2
			return
		if(self.goAround==2):
			self.x+=sin(tan_inv(self.target_y-self.y/self.target_x-self.x))
			self.y+=cos(tan_inv(self.target_y-self.y/self.target_x-self.x))
