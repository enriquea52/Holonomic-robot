#!/usr/bin/env python

import time
import rospy
from holo.msg import ind_coor


#ROS BEGINS
rospy.init_node('Pos_Est', anonymous=True)
pub = rospy.Publisher('/robot_pos', ind_coor, queue_size=10)




def mai():

	while(True):
		
		motion=ind_coor()
		time.sleep(1)
		motion.x=2
		motion.y=0
		pub.publish(motion)
		time.sleep(1)
		motion.x=0
		motion.y=2
		pub.publish(motion)
		time.sleep(2)


	

if __name__=='__main__':
	mai()




