#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time 
from math import *

rospy.init_node('calibration_node', anonymous=True)                   #
vel_msg = Twist()
pub = rospy.Publisher('RPM', Twist, queue_size=10) 

time.sleep(3)
distance = 1 #meters

max_vel = 0.118438 #best linear speed to consider

zeit = distance/max_vel

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
print("Done")


