#!/usr/bin/env python

#importing
import rospy

from geometry_msgs.msg import Pose
from sensor_msgs.msg import LaserScan
import numpy as np

#declaring the global variables, for ease of corrector to change values in case if there is a need to change
global Kp, L, emax, ee

Kp = 0.04
L = 1.0
emax = 0.3
ee = 1

pose=Pose()

#callback function from Laserscan, where in we get the data from the lidar
def received_msg(msg):
    global pose
    ranges = msg.ranges

    # converting it to numpy arrays
    npranges = np.array(ranges)

    #for the  NaN values 
    npranges[npranges > msg.range_max] = float('NaN')
    npranges[npranges < msg.range_min] = float('NaN')

    # to calculate the minimum distance and it angle of the object
    dis = np.nanmin(npranges)
    alpha_angle = np.reshape( np.argwhere(npranges == dis) , -1)
    
    #error calculating 
    error = dis - L
    

    #   if abs(error) > emax:
    #       emod 

    #according to the given condiotion 
    if error >= emax:
        ee = 1

    if (-emax) < error and error < emax:
        ee = error/emax
    
    if error <= (-emax):
        ee = -1
    
    # report the data
    pose.position.x = dis
    pose.position.y = error
    pose.position.z = ee          #!! 
    
    pose.orientation.x = Kp * ee
    pose.orientation.y = Kp * (1-abs(ee))        #!!
    
    pose.orientation.z = float((alpha_angle * msg.angle_increment)+msg.angle_min)
    
    #print("update", pose.position.x, pose.position.y, pose.position.z)
    
    #publishing the recieved values 
    publisher_obj.publish(pose)
    #print("data published")



rospy.init_node('sensed_object', anonymous=False)
rospy.Subscriber('/scan', LaserScan, received_msg)
publisher_obj=rospy.Publisher('/turtle1/sensed_object', Pose, queue_size=1)

while not rospy.is_shutdown():
    #Rate set to 10Hz as given in the question 
    rate=rospy.Rate(10)
    publisher_obj.publish(pose)
    rate.sleep()

#if __name__ == '__main__':
    #main_function()