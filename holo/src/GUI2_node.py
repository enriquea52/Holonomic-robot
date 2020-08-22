#!/usr/bin/env python


import rospy
import time
from holo.msg import coordinates
from holo.msg import path_points
from holo.msg import ind_coor
from holo.msg import current_angle
from holo.msg import numlist

from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

import subprocess

#################################################
#################################################
from turtle import *
from random import seed
from random import randint
import turtle
import math
from packages_lib.csv_reader import map_getter
#################################################
#################################################


flecha=turtle.Turtle()

#coori=(-150.0,0)
#coorf=(150.0,0)

coori=(150.0,-150.0) #Partially-Known map
coorf=(0.0,200.0)

#coori=(150.0,-200.0) #Known map
#coorf=(150.0,150.0)

#coori=(-150.0,-200.0) #Unknown map
#coorf=(150.0,150.0)

#coori=(150.0,150.0)
#coorf=(-150.0,-200.0)

robot_global_position=[coori[0],coori[1],(90*(pi)/180)] #configuring the initial pose of the robot

turtle.addshape("holo_robot.gif")
my_robot = turtle.Turtle()
my_robot.shape('holo_robot.gif')
my_robot.penup()
my_robot.goto(coori[0],coori[1])
my_robot.color("blue")
my_robot.pensize(5)


robot_av_env = []

pub = rospy.Publisher('positions', coordinates, queue_size=10)# RRT publisher

pub_ang = rospy.Publisher('/initial_angle', coordinates, queue_size=10)



distance_traveled = 0

#Funcion ////////////////////////////////////////////////////////
def puntos():
    inicio=[randint(-300, 300),randint(-300, 300)];
    final=[randint(-300, 300),randint(-300, 300)];
    return [inicio,final]

def nuevo(Ra_ro = 36):
    x=randint(-300+Ra_ro, 300-Ra_ro);
    y=randint(-300+Ra_ro, 300-Ra_ro);
    return[x,y]

def prueba (punto,area):
    x_obstaculos=[]
    y_obstaculos=[]
    for i in range(len(area)):
        j=area[i]
        if punto[0]>=j[0] and punto[0]<=(j[0]+j[2]) and punto[1]>=j[1] and punto[1]<=(j[1]+j[3]):
            return 0
    return 1

def dibuja_obstaculo(matriz):
    flecha.penup()
    for i in range(len(matriz)):
        objeto=matriz[i]
        flecha.begin_fill()
        flecha.goto(objeto[0],objeto[1])
        flecha.pendown()
        flecha.goto(objeto[0]+objeto[2],objeto[1])
        flecha.goto(objeto[0]+objeto[2],objeto[1]+objeto[3])
        flecha.goto(objeto[0],objeto[1]+objeto[3])
        flecha.goto(objeto[0],objeto[1])
        flecha.end_fill()
        flecha.penup()

def secciones(antes, nuevo,area):
    x_actual=antes[0]
    y_actual=antes[1]
    esc_x=(nuevo[0]-antes[0])/91
    esc_y=(nuevo[1]-antes[1])/91
    for i in range (90):
        for j in range (len(area)):
            obsta=area[j]
            if x_actual>=obsta[0] and x_actual<=(obsta[0]+obsta[2]) and y_actual>=obsta[1] and y_actual<=(obsta[1]+obsta[3]):
                return 0
        x_actual=x_actual+esc_x
        y_actual=y_actual+esc_y
    return 1

def calculo_Costo(costo,puntos,nodo,distancia,posicion):
    D_base=min(distancia)+radio_a;
    C_base=costo[posicion]
    for i in range(len(puntos)):
        test=distancia[i]
        C_new= costo[i]
        if test<=D_base and C_new<=C_base:
            cordenada=i 
    return cordenada

def dibujo(ruta):
    flecha.penup()
    s=ruta[0]
    flecha.goto(s[0],s[1])
    flecha.color("blue")
    flecha.pendown()
    for i in range(len(ruta)-1):
        segundo=ruta[i+1]
        flecha.goto(segundo[0],segundo[1]);
    

def dibujo2(ruta):
    flecha.penup()
    flecha.goto(ruta[0].x,ruta[0].y)
    flecha.color("red")
    flecha.pendown()
    for i in range(len(ruta)-1):
        flecha.goto(ruta[i+1].x,ruta[i+1].y)
	
	
	



def rrt_setup(xi,yi,xf,yf,campo):
    # ventana /////////////////////////////////////////////////////////////////////////
    setup(700,700, 0, 0)
    screensize(600, 600)
    title("Algoritmo RRT*")

    window = turtle.Screen()
    global flecha
    flecha.hideturtle()
    flecha.penup()
    flecha.goto(-300,310)
    flecha.pensize(2)
    flecha.pendown()
    flecha.forward(100)
    flecha.penup()
    flecha.goto(-300,-300)
    flecha.speed(60)
    flecha.pendown()
    flecha.pensize(3)
    for i in range(4):
        flecha.forward(600)
        flecha.left(90)

    #aqui se define el punto inicial y final
    inicio=[xi,yi];
    final=[xf,yf];

    #aqui se define el ambiente de trabajo
    flecha.penup()
    flecha.color("red")

      
    ##Obstaculos visibles
    dibuja_obstaculo(campo)


    flecha.goto(final[0],final[1]);flecha.dot((15),"green")
    flecha.goto(inicio[0],inicio[1]);flecha.dot((15),"gray")
    flecha.color("orange")
    #flecha.showturtle()

    #Comandos ///////////////////////////////////////////////////////////////////
    radio_a=100
    radio_b=50
    return radio_a,radio_b,[xi,yi],[xf,yf]

#ROS###############################################################################################################
rospy.init_node('GUI', anonymous=True)

import threading

def orientation_mod(msg):
	global robot_global_position

	robot_global_position[2] = msg.angle
	

def actual_trayectory(msg):
	dibujo2(msg.Path)


def agent_pos(msg):
	global robot_global_position
	global distance_traveled

	if (msg.linear.x < 10) : #Just updates will be taken into account when the x axis is not receiving ticks
		robot_global_position[0]=robot_global_position[0]+(cos(robot_global_position[2]))*((msg.linear.y)/105)
		robot_global_position[1]=robot_global_position[1]+(sin(robot_global_position[2]))*((msg.linear.y)/105)

	distance_traveled = distance_traveled+(msg.linear.y*(0.1885))/(4320.0)
	print("Distance travelled: ",distance_traveled, " meters")
	
	my_robot.color("blue")
	my_robot.pendown()
	

	my_robot.goto(robot_global_position[0],robot_global_position[1])


def ros_magic():
	rospy.spin()

def obstacle_avoidance(msg):

	
	global robot_av_env

	coor_msg = coordinates() #Useful for publishing coordinates to the RRT star algorithm

	subprocess.Popen(["roslaunch","holo","motion.launch"])# Motion node is reactivated
	subprocess.Popen(["rosnode","kill","/Obs_det"])# Obstacle detection is deactivated

	time.sleep(3)

	angle_msg = coordinates()#Useful for publishing angle to the Motion_node 
	angle_msg.angle = robot_global_position[2] #The current orientation is sent
	pub_ang.publish(angle_msg)
	time.sleep(0.05)

	x_obs = robot_global_position[0]+(cos(robot_global_position[2]))*(((msg.data)*300)/1500)
	y_obs = robot_global_position[1]+(sin(robot_global_position[2]))*(((msg.data)*300)/1500)

		

	#creating an stimated obstacle for avoidance considering an obstacle is 30cm by 30cm
	new_obstacle = [x_obs-20,y_obs,40,40]
	robot_av_env.append(new_obstacle)




	for i in robot_av_env:
		count = 0
		for j in i:
			if count == 0:
				i[count] = j-10
			if count == 1:
				i[count] = j-10
			if count == 2:
				i[count] = j+10
			if count == 3:
				i[count] = j+10
			count = count+1
			

	time.sleep(0.1)	
	flecha.color("red")
	dibuja_obstaculo(robot_av_env)

	for i in robot_av_env:
		obs = numlist()
		obs.ind_obs = i
		coor_msg.map.append(obs)


	#RRT* is implemented again 
	coor_msg.xi,coor_msg.yi,coor_msg.xf,coor_msg.yf = robot_global_position[0],robot_global_position[1],coorf[0],coorf[1] 

	time.sleep(0.05)

	#Sending coordinates to RRT*_node for the algorithm to work correctly

	pub.publish(coor_msg)



	

	
		
	

	
	
	
	

	

def node_behviour():

	global robot_av_env 
	

	rate = rospy.Rate(10) # 10hz
	coor_msg = coordinates() #Useful for publishing coordinates to the RRT star algorithm
	angle_msg = coordinates()#Useful for publishing angle to the Motion_node 

	rospy.Subscriber("/motion_path",path_points,actual_trayectory) ## Subscriber to get route
	rospy.Subscriber("ticks",Twist,agent_pos,queue_size = 100)## Subscriber to get robot position
	rospy.Subscriber("current_ori",current_angle,orientation_mod)## Subscriber to get robot position
	
	#the most important subscription
	rospy.Subscriber("avoidance",Int32,obstacle_avoidance)## Subscriber to get robot position

	robot_map='maps/hmap2.csv' #Map csv location is retrieved

	obs_list=map_getter(robot_map) #A list with the obstacles is obtained

	robot_av_env = obs_list #A global variables stroes all the obstacles 

	
	#RRT* first consideration for the first time
	radio_a,radio_b,inicio,final=rrt_setup(coori[0],coori[1],coorf[0],coorf[1],robot_av_env) 
	
	
	
	for i in robot_av_env:
		obs = numlist()
		obs.ind_obs = i
		coor_msg.map.append(obs)
		
		
	coor_msg.xi,coor_msg.yi,coor_msg.xf,coor_msg.yf = inicio[0],inicio[1],final[0],final[1]


	
	angle_msg.angle = robot_global_position[2] #The initial angle is retrieved 

	#Sending initial orientation to Motion_node for the algorithm to work correctly
	
	time.sleep(0.5)

	pub_ang.publish(angle_msg)
	time.sleep(0.5)

	#Sending initial coordinates to RRT*_node for the algorithm to work correctly

	pub.publish(coor_msg)

	time.sleep(0.5)

	

	x = threading.Thread(target=ros_magic)
	x.daemon = True
	x.start()

	turtle.mainloop()

	

if __name__ == '__main__':
	try:
		node_behviour()
	except rospy.ROSInterruptException:
		pass







