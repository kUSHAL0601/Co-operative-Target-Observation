import math
from random import random

class ObstacleClass:
	def __init__(self,position_x,position_y,angle,obs_id):
		self.x=position_x
		self.y=position_y
		self.angle=angle
		self.id=obs_id
