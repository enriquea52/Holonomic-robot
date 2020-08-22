#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np
import rospy
from kinect_obstacles.msg import kinect_data

rospy.init_node('kinect',anonymous=True)
pub = rospy.Publisher('/min_depth',kinect_data,queue_size=10)
depth_data=kinect_data()



def get_depth():
	return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])

def get_video():
	return frame_convert2.video_cv(freenect.sync_get_video()[0])

done = False

cut = 150 # number of rows or columns to be eliminated
rows = 480  #depth image number of rows
columns= 640 #depth image number of columns

print("Starting detection...")


fail=1
while(1):
	try:
		distances = freenect.sync_get_depth()[0]
		print("Node_Working")
		break
	except:
		pass
	
	



while not(done):
	
	distances = freenect.sync_get_depth()[0] # A raw depth image is obtained for further processing 
	
	# The foloowing three images are for visualization
	depth_vis = get_depth() # Pretty dept image
	image = get_video() # rgb image
	roi = depth_vis[cut+50:,cut:columns-cut] # Cropped pretty depth image for visualization
	
	distances = np.asarray(distances) #depth image is converted to numpy array
	roi_depth = distances[cut+50:,cut:columns-cut]# cropped image for eliminating noise
	
	
	filter_1 = np.amin(roi_depth,axis = 0) # the minimum distances from columns are retrieved (taking into consideration cropped depth image)
	
	depth_data.distances = filter_1  #Data is converted in custom ROS message
	pub.publish(filter_1) #Data is published
	
	#print(filter_1[filter_1 !=0].mean())
	#print(filter_1)
	#cv2.imshow('ROI', roi)
	#cv2.imshow('depth_vis', depth_vis)
	#cv2.imshow('RGB_IMAGE', image)
	
	if cv2.waitKey(10) == 27:
		break
	

