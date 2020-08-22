#!/usr/bin/env python

import pygame

from math import *
 
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 200,   0)
RED =   (200,   0,   0)
 
#initiall setup and variables
size = [700, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Holonomic drive robot planning and replanning")
done = False
clock = pygame.time.Clock()
resolution=10
sub=600
diff = (size[0]-sub)/2
step = (sub/resolution) - 1
screen.fill(WHITE)

def creating_grid():
	for i in range(0,resolution):
		pygame.draw.line(screen, BLACK, [0+diff, (i*step)+diff], [step*resolution+diff,(i*step)+diff], 1)
		pygame.draw.line(screen, BLACK, [(i*step)+diff,0+diff],[(i*step)+diff,step*resolution+diff], 1)
	pygame.draw.line(screen, BLACK, [0+diff, (resolution*step)+diff], [step*resolution+diff,(resolution*step)+diff], 1)
	pygame.draw.line(screen, BLACK, [(resolution*step)+diff,0+diff],[(resolution*step)+diff,step*resolution+diff], 1)
	for i in range(0,resolution+1):
		for j in range(0, resolution+1):
			pygame.draw.circle(screen, RED, (i*step+diff,j*step+diff), 5)
	pygame.display.flip()
			
			
creating_grid()	

coordinates=[(0,0),(0,0)]
coor_counter=0
#Main loop
while not done:
	# This limits the while loop to a max of 10 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(10)
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
			
	mouse = pygame.mouse.get_pos()

	#detectar cual coordenada se ha presionado
	for i in range(0,resolution+1):
		for j in range(0, resolution+1):
			if ((i*step+diff+5)>mouse[0]>(i*step+diff-5)) and ((j*step+diff+5)>mouse[1]>(j*step+diff-5)):
				pygame.draw.circle(screen, GREEN, (i*step+diff,j*step+diff), 5)
				pygame.display.flip()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						coordinates[coor_counter]=(i*step+diff,j*step+diff)
						print(coordinates[coor_counter])
						coor_counter=coor_counter+1
						
			else:
				pygame.draw.circle(screen, RED, (i*step+diff,j*step+diff), 5)
				pygame.display.flip()
	
	if coor_counter>1:
		break
	


xi=((coordinates[0][0]-diff)/step)
yi=abs(((coordinates[0][1]-diff)/step)-resolution)
xf=((coordinates[1][0]-diff)/step)
yf=abs(((coordinates[1][1]-diff)/step)-resolution)
print(xi,yi,xf,yf)

# Be IDLE friendly
pygame.quit()
