from __future__ import division
import pygame, sys
from pygame.locals import *
from math import *
import random
import math
from time import strftime

class Alg2:
	def __init__(self, radius, x_orig, y_orig):
		#Radius
		self.r = radius

		#Origin
		self.x0 = x_orig
		self.y0 = y_orig

		#Angles
		self.a1 = 0
		self.a2 = random.randint(0, 360)

		#First Robot
		self.x1 = x_orig
		self.y1 = y_orig

		#Second Robot
		self.r2 = random.randint(0, self.r)
		self.x2 = int(self.x0 + self.r2*cos(radians(self.a2)))
		self.y2 = int(self.y0 - self.r2*sin(radians(self.a2)))

		#Exit
		self.a3 = random.randint(0, 360)
		self.x3 = int(self.x0 + self.r*cos(radians(int(self.a3))))
		self.y3 = int(self.y0 - self.r*sin(radians(int(self.a3))))

		#Targets on cicle
		self.xt, self.yt, self.at = self.findCircle();

		#Directions
		self.d1 = 0.56
		self.d2 = -0.56

		#isReached
		self.reached = 0
		self.point = 0
		self.point1 = 0
		self.x_temp = 0
		self.y_temp = 0
		self.x_temp1 = 0
		self.y_temp1 = 0
		self.add = 0
		self.add1 = 0
		self.c = 0


	def steps(self):
		if(self.reached == 1):
			self.x_temp = self.x2
			self.y_temp = self.y2
			self.point = 0
			val = math.sqrt((self.x3-self.x2)**2 + (self.y3-self.y2)**2)
			self.add = (1 / val) if val != 0 else 0
		if(self.reached == 2):
			self.x_temp = self.x1
			self.y_temp = self.y1
			self.point = 0
			val = math.sqrt((self.x3-self.x1)**2 + (self.y3-self.y1)**2)
			self.add = (1 / val) if val != 0 else 0

	def circle_steps(self):
		self.x_temp = self.x1
		self.y_temp = self.y1
		self.x_temp1 = self.x2
		self.y_temp1 = self.y2
		self.a1 = self.at
		self.a2 = self.at
		self.point = 0
		self.point1 = 0
		val = math.sqrt((self.xt-self.x1)**2 + (self.yt-self.y1)**2)
		self.add = (1 / val) if val != 0 else 0
		val = math.sqrt((self.xt-self.x2)**2 + (self.yt-self.y2)**2)
		self.add1 = (1 / val) if val != 0 else 0


	def to_circle(self):
		if(self.point <= 1):
			self.x1 = int(self.x_temp + self.point*(self.xt - self.x_temp))
			self.y1 = int(self.y_temp + self.point*(self.yt - self.y_temp))
		if(self.point1 <= 1):
			self.x2 = int(self.x_temp1 + self.point1*(self.xt - self.x_temp1))
			self.y2 = int(self.y_temp1 + self.point1*(self.yt - self.y_temp1))
		if(self.point > 1 and self.point1 > 1):
			self.x1 = self.xt
			self.y1 = self.yt
			self.x2 = self.xt
			self.y2 = self.yt
			return False
		else:
			self.point += self.add
			self.point1 += self.add1
			return True
		

	def to_target(self):
		if(int(self.a1 % 360) == self.a3 or
			(self.x1 == self.x3) and (self.y1 == self.y3)):
			self.reached = 1
			return False
		elif(int(self.a2 % 360) == self.a3 or
			(self.x2 == self.x3) and (self.y2 == self.y3)):
			self.reached = 2
			return False
		else:
			self.x1 = int(self.x0 + self.r*cos(radians(self.a1)))
			self.y1 = int(self.y0 - self.r*sin(radians(self.a1)))

			self.x2 = int(self.x0 + self.r*cos(radians(self.a2)))
			self.y2 = int(self.y0 - self.r*sin(radians(self.a2)))

			self.a1 += self.d1
			self.a2 += self.d2
			return True

	def mid_point(self, a1, a2):
		between = abs(a1 - a2)
		ang = a1 + (between / 2) if (a1 < a2) else a2 + (between / 2)
		if(a1 < 90 and a2 > 270):
			between = 360 - between
			ang = a1 - (between / 2)
			if(ang < 0):
				ang = 360 + ang
		if(a2 < 90 and a1 > 270):
			between = 360 - between
			ang = a2 - (between / 2)
			if(ang < 0):
				ang = 360 + ang
		return ang

	def findCircle(self):
		a3 = int(self.mid_point(self.a1, self.a2))
		x3 = int(self.x0 + self.r*cos(radians(int(a3))))
		y3 = int(self.y0 - self.r*sin(radians(int(a3))))
		return (x3, y3, a3)

	def call_robot(self):
		if(self.reached == 1):
			if(self.point < 1):
				self.x2 = int(self.x_temp + self.point*(self.x3 - self.x_temp))
				self.y2 = int(self.y_temp + self.point*(self.y3 - self.y_temp))
				self.point += self.add
				return True
			else:
				self.x2 = self.x3
				self.y2 = self.y3
				return False
		if(self.reached == 2):
			if(self.point < 1):
				self.x1 = int(self.x_temp + self.point*(self.x3 - self.x_temp))
				self.y1 = int(self.y_temp + self.point*(self.y3 - self.y_temp))
				self.point += self.add
				self.c += 1
				return True
			else:
				self.x1 = self.x3
				self.y1 = self.y3
				return False

	def log_file(self, time, num):
		date = strftime("%Y-%m-%d %H:%M:%S")
		title = "./lib/logs/a2/"+date + "_Alg2"
		file = open(title, "w")
		file.write("Date: " +date + "\n")
		file.write("Number of Executions: " + str(num) + "\n")
		file.write("Time total: " + str(time) + "\n")
		file.close()





	def robot_1(self):
		return (int(self.x1), int(self.y1))

	def robot_2(self):
		return (int(self.x2), int(self.y2))

	def exit(self):
		return (int(self.x3), int(self.y3))
