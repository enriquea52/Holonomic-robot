#!/usr/bin/env python


import rospy
import time
from holo.msg import coordinates
from holo.msg import path_points
from holo.msg import ind_coor
from geometry_msgs.msg import Twist

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

coori=(-150.0,-200.0)
coorf=(150.0,150.0)

#coori=(150.0,150.0)
#coorf=(-150.0,-200.0)

robot_global_position=[coori[0],coori[1]]

turtle.addshape("holo_robot.gif")
my_robot = turtle.Turtle()
my_robot.shape('holo_robot.gif')
my_robot.penup()
my_robot.goto(coori[0],coori[1])



#Funcion ////////////////////////////////////////////////////////
def puntos():
    inicio=[randint(-300, 300),randint(-300, 300)];
    final=[randint(-300, 300),randint(-300, 300)];
    return [inicio,final]

def nuevo():
    x=randint(-300, 300);
    y=randint(-300, 300);
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
        flecha.goto(ruta[i+1].x,ruta[i+1].y);



def rrt_setup(xi,yi,xf,yf,map_csv):
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
    campo=map_getter(map_csv)
      
    ##Obstaculos visibles
    dibuja_obstaculo(campo)


    flecha.goto(final[0],final[1]);flecha.dot((15),"green")
    flecha.goto(inicio[0],inicio[1]);flecha.dot((15),"gray")
    flecha.color("orange")
    #flecha.showturtle()

    #Comandos ///////////////////////////////////////////////////////////////////
    radio_a=100
    radio_b=50
    return campo,radio_a,radio_b,[xi,yi],[xf,yf]

#ROS###############################################################################################################
rospy.init_node('GUI', anonymous=True)

import threading

def actual_trayectory(msg):
	print(msg.Path)
	dibujo2(msg.Path)


def agent_pos(msg):
	global robot_global_position
	if (msg.angular.x == 1):
		robot_global_position[0]=robot_global_position[0]+((msg.linear.x)/114.6)
	elif (msg.angular.x == 0):
		robot_global_position[0]=robot_global_position[0]-((msg.linear.x)/114.6)
	if (msg.angular.y == 1):
		robot_global_position[1]=robot_global_position[1]+((msg.linear.y)/114.6)
	elif (msg.angular.y == 0):
		robot_global_position[1]=robot_global_position[1]-((msg.linear.y)/114.6)
	
	my_robot.goto(robot_global_position[0],robot_global_position[1])


def ros_magic():
	rospy.spin()

	

def node_behviour():
	pub = rospy.Publisher('/positions', coordinates, queue_size=10)
	rate = rospy.Rate(10) # 10hz
	coor_msg = coordinates()

	rospy.Subscriber("/motion_path",path_points,actual_trayectory) ## Subscriber to get route
	rospy.Subscriber("ticks",Twist,agent_pos,queue_size = 1000)## Subscriber to get robot position

	robot_map='maps/map1.csv'
	
	campo,radio_a,radio_b,inicio,final=rrt_setup(coori[0],coori[1],coorf[0],coorf[1],robot_map)

	coor_msg.xi,coor_msg.yi,coor_msg.xf,coor_msg.yf,coor_msg.map = inicio[0],inicio[1],final[0],final[1],robot_map

	time.sleep(2)

	pub.publish(coor_msg)

	turtle.mainloop()

	x = threading.Thread(target=ros_magic)
	x.daemon = True
	x.start()

	

if __name__ == '__main__':
	try:
		node_behviour()
	except rospy.ROSInterruptException:
		pass







