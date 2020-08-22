#!/usr/bin/env python

import rospy 
import numpy as np
from kinect_obstacles.msg import kinect_data
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import os, signal,time,subprocess

rospy.init_node('obs_detect',anonymous=True)
pub = rospy.Publisher('RPM', Twist, queue_size=10)     

pub_detect = rospy.Publisher('avoidance', Int32, queue_size=10)     

motion_pid =100000000000000000000



def pid_to_kill(msg):
	global motion_pid
	
	motion_pid = msg.data
	#print(motion_pid)
	

def decision(msg):
	vel_msg = Twist()
	
	distances=np.asarray(msg.distances) # ROS message conversion to numpy array
	mean_distance=(distances[distances !=0].mean()) #Mean dsitance from depth image without considering 0 values
	print(mean_distance)
	
	if mean_distance<=600:  #If distance is equal or less than 60 cm
		print("detener")
		
		#Kill motion node
		try:
		        subprocess.Popen(["rosnode","kill","/Robot_Motion"])	
                        #os.kill(motion_pid, signal.SIGKILL)
		except:
			pass
		#Stop robot motion completely
		vel_msg.linear.x=0
		vel_msg.linear.y=0
		vel_msg.linear.z=0
		vel_msg.angular.x=0
		vel_msg.angular.y=0
		vel_msg.angular.z=0
		time.sleep(0.02)
		pub.publish(vel_msg) #Sen message to TIVA  to stop robot
		
		obs_dist=Int32()
		obs_dist.data = mean_distance

		pub_detect.publish(obs_dist)
                time.sleep(1)




def detection():

	rospy.Subscriber("min_depth",kinect_data,decision)
	rospy.Subscriber("pid_name",Int32,pid_to_kill)
	print("Node ready")
	rospy.spin()


if __name__=='__main__':
	detection()

