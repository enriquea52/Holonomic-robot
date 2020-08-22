#!/usr/bin/env python
from packages_lib.RRT_ROBOT import *
import rospy
from holo.msg import coordinates
from holo.msg import path_points
from holo.msg import ind_coor

######  Node initialization   #######################################   
rospy.init_node('RRT', anonymous=True)	                            #
								    #
#####################Publisher to GUI NODESetup######################
#####################Publisher to Motion NODESetup####################
								     #
			                                             #
pub_Motion = rospy.Publisher('/motion_path', path_points, queue_size=10)#
trayectory_msg_motion = path_points()		                     #
								     #
######################################################################




def callback(data):
 
	campo = []
	for i in data.map:
		campo.append(i.ind_obs)

	# -300 to 300 coordinate system
	ruta=rrt(campo,100,50,[data.xi,data.yi],[data.xf,data.yf],36)
	new_ruta=optimisar(ruta,campo)
	#position from -300-300 coordinate system   #### to robot motion
	for coordinate in new_ruta:
		point=ind_coor()
		point.x=coordinate[0]
		point.y=coordinate[1]
		trayectory_msg_motion.Path.append(point)

		
	pub_Motion.publish(trayectory_msg_motion)
	del trayectory_msg_motion.Path[:]


	print(new_ruta)

def main():
	rospy.Subscriber("positions", coordinates, callback)
	rospy.spin()

if __name__ == '__main__':
	main()

