import math
from random import random

class TargetsClass:
	def __init__(self,position_x,position_y,speed,angle):
		self.x=position_x
		self.y=position_y
		self.speed=speed
		self.angle=angle

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
	def predict(self,x_limit,y_limit):
		temp_x=self.x+self.speed*math.cos(self.angle)
		temp_y=self.y+self.speed*math.sin(self.angle)
		if(temp_x>x_limit or temp_x<-x_limit):
			temp_x=self.x+(random()*(x_limit/2)-(x_limit/4))
		if(temp_y>y_limit or temp_y<-y_limit):
			temp_y=self.y+(random()*(x_limit/2)-(x_limit/4))
		return (temp_x,temp_y)
