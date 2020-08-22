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
from holo.msg import coordinates
from holo.msg import current_angle
from std_msgs.msg import Int32

import subprocess


###################################################################
rospy.init_node('Robot_Motion', anonymous=True)                   #
pub = rospy.Publisher('RPM', Twist, queue_size=10)                # this publisher publishes the motion rules to the 									  # TIVA for proper motion
###################################################################
angle_pub = rospy.Publisher('current_ori', current_angle, queue_size=10)         # This publisher publishes the current orientation 									    for grafical interaction  
pid_pub = rospy.Publisher('pid_name', Int32, queue_size=10)         # This publisher publishes the pid number of this node to be killed when required


robot_angle = 0
activation =0

def robot_initials(msg):
	global robot_angle

	robot_angle = (msg.angle)

	return




def motion_sender(msg):

	global robot_angle
	global activation

	#Variables of importance
	mov_x=0
	mov_y=0
	rot_z=0
	zeit_mov=0
	zeit_rot=0

	
	#rot_z,zeit_rot = angular_mo(percent,angle)

	#Declaration of messages to be used
	vel_msg = Twist()     
	angle_msg = current_angle()                                     


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

		angle_msg.angle = turn_angle_radian
		angle_pub.publish(angle_msg) # Here the current angle with respect the global coordinate system is 						       being published to the GUI node.

		robot_angle_rot = robot_angle-turn_angle_radian


		zeit = abs((robot_angle_rot)/(0.87408118081)) #time for reaching certain angle with angular speed
		robot_angle = turn_angle_radian

		#Message Varaibles for angular motion / Orientation
		vel_msg.linear.x = 40
		vel_msg.linear.y = 40
		vel_msg.linear.z = 0
		if (robot_angle_rot < 0):
			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = 2
		if (robot_angle_rot > 0):
			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = 1

		time.sleep(0.02)
		pub.publish(vel_msg)
		print(zeit)
		time.sleep(zeit)
		
		#if activation == 0:
		#	subprocess.Popen(["roslaunch","holo","detect.launch"])# Detection node is reactivated
		#	activation=activation+1
		

		vel_msg.linear.x=0
		vel_msg.linear.y=0
		vel_msg.linear.z=0
		vel_msg.angular.x=0
		vel_msg.angular.y=0
		vel_msg.angular.z=0
		pub.publish(vel_msg)		
		
		time.sleep(1)
		
		zeit = distance/(0.118438) #time for reaching certain distance with linear speed


		#Message Varaibles for forward motion
		vel_msg.linear.x = 0
		vel_msg.linear.y = 40
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 1
		vel_msg.angular.z = 0

		time.sleep(0.02)
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
	rospy.Subscriber("/initial_angle",coordinates,robot_initials)
	time.sleep(0.5)
	



	rospy.spin()	



if __name__ == '__main__':
	try:
		path_subscriber()
		
	except rospy.ROSInterruptException:
		pass


