import math

class ObserverClass:
	def __init__(self,position_x,position_y,speed,sensor_range):
		self.x=position_x
		self.y=position_y
		self.speed=speed
		self.limit=sensor_range

	def set_angle(self,target_x,target_y):
		self.angle=math.atan((target_y-self.y)/(target_x-self.x))

	def update(self,x_limit,y_limit):
		temp_x=self.x+self.speed*math.cos(self.angle)
		temp_y=self.y+self.speed*math.sin(self.angle)
		if(temp_x>x_limit):
			temp_x=x_limit
		if(temp_y>y_limit):
			temp_y=y_limit
		self.x=temp_x
		self.y=temp_y

	def enemy_in_range(self,enemy):
		if(math.sqrt(pow(enemy.x-self.x,2)+pow(enemy.y-self.y,2))<=self.limit):
			return True
		else:
			return False
