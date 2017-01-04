from __future__ import division
import pygame, sys, os
from pygame.locals import *
from math import *
import random
from time import strftime

class Alg1:
	def __init__(self, radius, x_orig, y_orig):
		#Angles
		self.a1 = 0
		self.a2 = 0

		#First Robot
		self.x1 = x_orig
		self.y1 = y_orig

		#Second Robot
		self.x2 = x_orig
		self.y2 = y_orig

		#Radius
		self.r = radius

		#Origin
		self.x0 = x_orig
		self.y0 = y_orig

		#Exit
		self.a3 = random.randint(0, 360)
		self.x3 = int(self.x0 + self.r*cos(radians(int(self.a3))))
		self.y3 = int(self.y0 - self.r*sin(radians(int(self.a3))))

		#Directions
		self.d1 = 0.56
		self.d2 = -0.56

		#isReached
		self.reached = 0

		self.stepx = 0
		self.stepy = 0


	def to_circle(self):
		if(self.y1 != (self.y0 - self.r)):
			self.y1 -= 1
			self.y2 -= 1
			return True
		else:
			self.a1 = 90
			self.a2 = 90
			return False

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

	def steps(self):
		self.stepx = 0
		self.stepy = 0
		if(self.reached == 1):
			steps = max(abs(self.x1 - self.x2), abs(self.y1 - self.y2))
			if steps != 0:
				self.stepx = float(self.x1 - self.x2)/steps
				self.stepy = float(self.y1 - self.y2)/steps
		if(self.reached == 2):
			steps = max(abs(self.x2 - self.x1), abs(self.y2 - self.y1))
			if steps != 0:
				self.stepx = float(self.x2 - self.x1)/steps
				self.stepy = float(self.y2 - self.y1)/steps


	def call_robot(self):
		if(self.reached == 1):
			self.x2 += int(self.stepx)
			self.y2 += int(self.stepy)
			if((self.x1, self.y1) == (self.x2, self.y2)):
				return False
			else:
				return True
		elif(self.reached == 2):
			self.x1 += int(self.stepx)
			self.y1 += int(self.stepy)
			if((self.x1, self.y1) == (self.x2, self.y2)):
				return False
			else:
				return True

	
	def log_file(self, time, num):
		date = strftime("%Y-%m-%d %H:%M:%S")
		title = "./lib/logs/a1/"+date + "_Alg1"
		file = open(title, "w")
		file.write("Date: " +date + "\n")
		file.write("Execution number: " + str(num) + "\n")
		file.write("Time total: " + str(time) + "\n")

		file.close()

		


	def robot_1(self):
		return (self.x1, self.y1)

	def robot_2(self):
		return (self.x2, self.y2)

	def exit(self):
		return (self.x3, self.y3)
