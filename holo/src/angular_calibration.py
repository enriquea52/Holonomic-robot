#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time 
from math import *

rospy.init_node('calibration_node', anonymous=True)                   #
vel_msg = Twist()
pub = rospy.Publisher('RPM', Twist, queue_size=10) 

time.sleep(3)

angle = 90 #degrees

max_vel = 0.118438 #best linear speed to consider

robot_r = 0.1355

w = max_vel/robot_r
print("Angular: ",w)

zeit = ((angle*pi)/180)/w

#Message Varaibles for forward motion
vel_msg.linear.x = 40
vel_msg.linear.y = 40
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 1

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
print("Done")


