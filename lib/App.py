from __future__ import division
import pygame, sys
from pygame.locals import *
from math import *
import random
import alg1
import alg2
import alg3
import time
import eztext

class App:

	def __init__(self):
		self.width = 700
		self.height = 500

		self.white = (255,255,255)
		self.grey = (100, 100, 100)
		self.black = (75, 75, 75)
		self.blue = (135,206,250)
		self.color1 = (0,0,139)
		self.color2 = (100, 50, 100)
		self.color3 = (255, 0, 0)
		self.background = (230,230,230)
		self.r = 100

		#Origin
		self.x0 = 250
		self.y0 = 200

		self.b_colors = [self.blue, self.blue, self.blue, self.blue, self.blue]
		self.algs = [alg1.Alg1(self.r, self.x0, self.y0), 
				alg2.Alg2(self.r, self.x0, self.y0), 
				alg3.Alg3(self.r, self.x0, self.y0)]

		self.num = -1
		self.font = 0
		self.screen= pygame.display.set_mode((self.width,self.height),0,32)

		self.txtbx = 0
		self.events = pygame.event.get()
		self.selected = 0


	def update(self):
		self.screen.lock()
		self.screen.fill(self.background)
		pygame.draw.circle(self.screen, self.black, (self.x0,self.y0), self.r, 4)
		pygame.draw.circle(self.screen, self.black, (self.x0,self.y0), 4, 0)


		#Buttons
		pygame.draw.rect(self.screen, self.b_colors[0],(500,100,150,50), 0)
		pygame.draw.rect(self.screen, self.b_colors[1],(500,200,150,50), 0)
		pygame.draw.rect(self.screen, self.b_colors[2],(500,300,150,50), 0)
		pygame.draw.rect(self.screen, self.b_colors[3] ,(50,400,150,50), 0)
		pygame.draw.rect(self.screen, self.b_colors[4] ,(300,400,150,50), 0)

		if self.num > -1:
			pygame.draw.circle(self.screen, self.color1, self.algs[self.num].robot_1(), 4, 0)
			pygame.draw.circle(self.screen, self.color2, self.algs[self.num].robot_2(), 4, 0)
			pygame.draw.circle(self.screen, self.color3, self.algs[self.num].exit(), 4, 0)

		self.screen.unlock()
		#self.txtbx.draw(screen)
		self.screen.blit(self.font.render('Algorithm 1', True, (0,0,0)), (525, 110))
		self.screen.blit(self.font.render('Algorithm 2', True, (0,0,0)), (525, 210))
		self.screen.blit(self.font.render('Algorithm 3', True, (0,0,0)), (525, 310))
		self.screen.blit(self.font.render('Start', True, (0,0,0)), (100, 410))
		self.screen.blit(self.font.render('Start Test', True, (0,0,0)), (340, 410))

		self.txtbx.set_pos(500, 410)
		self.txtbx.update(self.events)
		self.txtbx.set_font(self.font)
		self.txtbx.draw(self.screen)
		pygame.display.set_caption('Robot Evacuation')
		pygame.display.update()

	def clear_colors(self):
		for i in range(4):
			self.b_colors[i] = self.blue

	def buttons_colors(self, ind):
		self.clear_colors()
		self.b_colors[ind] = self.grey

	def start_visual(self):
		start = time.time()
		stat = True
		if(self.num > 0):
			self.algs[self.num].circle_steps()
		while stat:
			stat = self.algs[self.num].to_circle()
			self.update()
		stat = True
		while stat:
			stat = self.algs[self.num].to_target()
			self.update()
		stat = True
		self.algs[self.num].steps()
		while stat:
			stat = self.algs[self.num].call_robot()
			self.update()
		end = time.time()
		total = (end - start)
		self.algs[self.num].log_file(total, 1)

	def gen_alg(self,num):
		if(num == 0):
			self.algs[num] = alg1.Alg1(self.r, self.x0, self.y0)
		if(num == 1):
			self.algs[num] = alg2.Alg2(self.r, self.x0, self.y0)
		if(num == 2):
			self.algs[num] = alg3.Alg3(self.r, self.x0, self.y0)

	def start_test(self):
		num = self.txtbx.get_value()
		if(num == '' or num < 0):
			num = 0
		num = int(num)
		total = 0
		for i in range(num):
			start = time.time()
			stat = True
			if(self.num > 0):
				self.algs[self.num].circle_steps()
			while stat:
				stat = self.algs[self.num].to_circle()
				self.update()
			stat = True
			while stat:
				stat = self.algs[self.num].to_target()
				self.update()
			stat = True
			self.algs[self.num].steps()
			while stat:
				stat = self.algs[self.num].call_robot()
				self.update()
			self.gen_alg(self.num)
			end = time.time()
			total += (end - start)
		average = total / num
		self.algs[self.num].log_file(average, num)
		self.selected = 0
		self.clear_colors()


	def start(self):
		pygame.init()
		self.font = pygame.font.SysFont('Avenir', 18)
		self.txtbx = eztext.Input(maxlength=45, color=(0,0,0), prompt='Num: ')
		while True:
			self.events = pygame.event.get()
			for event in self.events:
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					posx, posy = pygame.mouse.get_pos()

					if(posx > 500 and posx < 650):
						if(posy > 100 and posy < 150):
							self.buttons_colors(0)
							self.num = 0
							self.algs[self.num] = alg1.Alg1(self.r, self.x0, self.y0)
							self.selected = 1
						if(posy > 200 and posy < 250):
							self.buttons_colors(1)
							self.num = 1
							self.algs[self.num] = alg2.Alg2(self.r, self.x0, self.y0)
							self.selected = 1
						if(posy > 300 and posy < 350):
							self.buttons_colors(2)
							self.num = 2
							self.algs[self.num] = alg3.Alg3(self.r, self.x0, self.y0)
							self.selected = 1
					if(posy > 400 and posy < 450):
						if(posx > 50 and posx < 200):
							if(self.selected == 1):
								self.start_visual()
								self.clear_colors()
								self.selected = 0
						if(posx > 300 and posx < 450):
							if(self.selected == 1):
								self.start_test()
								self.clear_colors()
								self.selected = 0
			self.update()


