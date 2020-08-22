#!/usr/bin/env python

import pygame

from math import *
from holo.msg import coordinates
from csv_reader import *
import time

class Environment():


	pygame.init()

	def __init__(self,h=700,w=700,resolution =20, sub = 600):
		self.h=h
		self.w=w
		self.resolution = resolution
		self.sub = sub

		self.BLACK = (  0,   0,   0)
		self.WHITE = (255, 255, 255)
		self.BLUE =  (  0,   0, 255)
		self.GREEN = (  0, 200,   0)
		self.RED =   (200,   0,   0)
		
		self.diff = 0
		self.step = 0
		

	def pygame_init(self):
		h=self.h
		w=self.w
		#initiall setup and variables
		size = [h,w]
		self.screen = pygame.display.set_mode(size)
		pygame.display.set_caption("Holonomic drive robot planning and replanning")
		self.diff = (size[0]-self.sub)/2
		self.step = (self.sub/self.resolution) - 1
		self.screen.fill(self.WHITE)
		pygame.display.flip()



	def creating_grid(self):
		diff=self.diff
		for i in range(0,self.resolution):
			pygame.draw.line(self.screen, self.BLACK, [0+diff, (i*self.step)+diff], [self.step*self.resolution+diff,(i*self.step)+diff], 1)
			pygame.draw.line(self.screen, self.BLACK, [(i*self.step)+diff,0+diff],[(i*self.step)+diff,self.step*self.resolution+diff], 1)
		pygame.draw.line(self.screen, self.BLACK, [0+diff, (self.resolution*self.step)+diff], [self.step*self.resolution+diff,(self.resolution*self.step)+diff], 1)
		pygame.draw.line(self.screen, self.BLACK, [(self.resolution*self.step)+diff,0+diff],[(self.resolution*self.step)+diff,self.step*self.resolution+diff], 1)
		for i in range(0,self.resolution+1):
			for j in range(0, self.resolution+1):
				pygame.draw.circle(self.screen, self.RED, (i*self.step+diff,j*self.step+diff), 5)
		pygame.display.flip()

	def creating_grid_2(self):
		diff=self.diff
		for i in range(0,self.resolution):
			pygame.draw.line(self.screen, self.BLACK, [0+diff, (i*self.step)+diff], [self.step*self.resolution+diff,(i*self.step)+diff], 1)
			pygame.draw.line(self.screen, self.BLACK, [(i*self.step)+diff,0+diff],[(i*self.step)+diff,self.step*self.resolution+diff], 1)
		pygame.draw.line(self.screen, self.BLACK, [0+diff, (self.resolution*self.step)+diff], [self.step*self.resolution+diff,(self.resolution*self.step)+diff], 1)
		pygame.draw.line(self.screen, self.BLACK, [(self.resolution*self.step)+diff,0+diff],[(self.resolution*self.step)+diff,self.step*self.resolution+diff], 1)
		pygame.display.flip()


	def initial_input(self):
		coordinates1=[(0,0),(0,0)]
		coor_counter=0
		diff =self.diff
		step = self.step
		resolution =self.resolution
		print("hola")

		while True:
			for event in pygame.event.get():
				pass 
		
			mouse = pygame.mouse.get_pos()
			#detectar cual coordenada se ha presionado


			for i in range(0,resolution+1):
				for j in range(0, resolution+1):
					if ((i*step+diff+5)>mouse[0]>(i*step+diff-5)) and ((j*step+diff+5)>mouse[1]>(j*step+diff-5)):
						pygame.draw.circle(self.screen, self.GREEN, (i*step+diff,j*step+diff), 5)
						pygame.display.flip()
						if event.type == pygame.MOUSEBUTTONUP:
							if event.button == 1:
								coordinates1[coor_counter]=(i*step+diff,j*step+diff)
								print(coordinates1[coor_counter])
								time.sleep(0.8)
								coor_counter=coor_counter+1
						
					else:
						pygame.draw.circle(self.screen, self.RED, (i*step+diff,j*step+diff), 5)
						pygame.display.flip()
			if coor_counter>1:
				break


		xi=(coordinates1[0][0]-diff)/float(step*(resolution/10))
		yi=abs(((coordinates1[0][1]-diff)/step)-resolution)/float(resolution/10)
		xf=(coordinates1[1][0]-diff)/float(step*resolution/10)
		yf=abs(((coordinates1[1][1]-diff)/step)-resolution)/float(resolution/10)
		print(xi,yi,xf,yf)
		return(xi,yi,xf,yf)

	def draw_path(self,path):
		self.path=path
		diff=self.diff
		step=self.step
		sub = self.sub
		resolution = self.resolution
		for i in range(0,len(path)-1):
			pygame.draw.line(self.screen, self.BLUE, [(path[i].x*step*(resolution/10)+diff),(((resolution/(resolution/10)-path[i].y)*step*(resolution/10)+diff))],[(path[i+1].x*step*(resolution/10)+diff),(((resolution/(resolution/10)-path[i+1].y)*step*(resolution/10)+diff))], 3)
		pygame.display.flip()

	def clear_screen(self):
		self.screen.fill(self.WHITE)
		self.creating_grid_2()
		pygame.display.flip()

	def map_val(x, in_min,in_max, out_min, out_max):
		return ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


	def draw_robot(self,x,y):
		pygame.draw.circle(self.screen, self.BLUE, (int(x),int(y)), 10)
		pygame.display.flip()


		
		
		
		
		

		
		

