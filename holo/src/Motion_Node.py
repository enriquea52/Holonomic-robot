#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time 
from math import *
####################################################
from packages_lib.RRT_ROBOT import *              ##
####################################################
from holo.msg import path_points
from holo.msg import ind_coor

###################################################################
rospy.init_node('Robot_Motion', anonymous=True)                   #
pub = rospy.Publisher('RPM', Twist, queue_size=10)    #
###################################################################



def linear_mo(d, angle):
	rpm = 40
	r = 0.03
	dirx=0
	diry=0
	vel= (((rpm*2.0*3.1426)/60.0)*0.03)

	yrpm=sin(angle)*rpm #y rpm
	xrpm=cos(angle)*rpm #x rpm

	yvel=sin(angle)*vel #y speed in m/s
	xvel=cos(angle)*vel #x speed in m/s
	
	Tvel=sqrt(pow(yvel,2)+pow(xvel,2))
	t=d/Tvel

	
	if (yrpm<0):
		diry = 0
	elif (yrpm>0):
		diry = 1
	if (xrpm<0):
		diry = 0
	elif (xrpm>0):
		dirx = 1

	return abs(int(xrpm)),abs(int(yrpm)),t,dirx,diry

def angular_mo(percent,angle):
	if percent>100:
		percent = 100
	elif percent<0:
		percent = 0

	linear_speed=(percent*0.377)/100
	angular_rad= linear_speed/0.142
	angular_degrees = angular_rad*(180/pi)

	t = angle/angular_degrees
	return int((percent*255)/100),t




def motion_sender(msg):
	#Variables of importance
	mov_x=0
	mov_y=0
	rot_z=0
	zeit_mov=0
	zeit_rot=0

	
	#rot_z,zeit_rot = angular_mo(percent,angle)


	vel_msg = Twist()                                         


	#variables to be used
	x_comp=0
	y_comp=0
	turn_angle_degree=0 #given in degrees
	turn_angle_radian = 0#given in radian
	mag=0
	distance= 0
	xm=1.5 #meters by 300 pixels
	velx=0
	vely=0
	Tvel=0
	zeit=0



	for i in range(0,len(msg.Path)-1):
		x_comp=msg.Path[i+1].x-msg.Path[i].x
		y_comp=msg.Path[i+1].y-msg.Path[i].y
		mag =  sqrt(pow(x_comp,2)+pow(y_comp,2))
		distance = (mag*xm)/300 # distance in meters

		turn_angle_degree=atan2(y_comp, x_comp)*(180/pi)
		turn_angle_radian=atan2(y_comp, x_comp)

		mov_x,mov_y,zeit,dir_x,dir_y = linear_mo(distance,turn_angle_radian) #radian angle used
		#Message Varaibles
		vel_msg.linear.x=mov_x
		vel_msg.linear.y=mov_y
		vel_msg.linear.z=0
		vel_msg.angular.x=dir_x
		vel_msg.angular.y=dir_y
		vel_msg.angular.z=0
		time.sleep(0.01)
		print(mov_x,mov_y,zeit)
		pub.publish(vel_msg)
		time.sleep(zeit)
	#Message Varaibles
	vel_msg.linear.x=0
	vel_msg.linear.y=0
	vel_msg.linear.z=0
	vel_msg.angular.x=0
	vel_msg.angular.y=0
	vel_msg.angular.z=0
	pub.publish(vel_msg)

	
def path_subscriber():
	rospy.Subscriber("/motion_path",path_points,motion_sender)	
	rospy.spin()	



if __name__ == '__main__':
	try:
		path_subscriber()
		
	except rospy.ROSInterruptException:
		pass


