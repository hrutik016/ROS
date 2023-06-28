#!/usr/bin/env python

#importing
import rospy

from geometry_msgs.msg import Pose
from sensor_msgs.msg import LaserScan
import numpy as np

#declaring the global variables, for ease of corrector to change values in case if there is a need to change
global x,theta,L,emax,Kp,emod
Kp=0.03
L=1.0
emax=0.3
e_mod=1

pose=Pose()

def received_msg(msg):
    global pose
    ranges = msg.ranges

    # converting it to numpy arrays
    npranges = np.array(ranges)

    # NaN values 
    npranges[npranges > msg.range_max] = float('NaN')
    npranges[npranges < msg.range_min] = float('NaN')

    # to calculate the minimum distance and it angle of the object
    dis = np.nanmin(npranges)
    alpha_angle = np.reshape( np.argwhere(npranges == dis) , -1)
    
    #error
    error = dis - L
    

    #   if abs(error) > emax:
    #       emod 

    #accordinf to the given condiotion 
    if error > emax:
        e_mod = 1
    if (-emax) <= error and error <= emax:
        e_mod = error/emax
    if error < (-emax):
        e_mod = -1
    # report the data

    #
    #e_mod = error / emax
    
    pose.position.x = dis
    pose.position.y = error
    pose.position.z = e_mod
    
    pose.orientation.x = Kp * e_mod
    pose.orientation.y = Kp * (1-abs(e_mod))        #!!
    
    pose.orientation.z = float((alpha_angle * msg.angle_increment) + msg.angle_min)
    
    print("update", pose.position.x, pose.position.y, pose.position.z)
    
    publisher_obj.publish(pose)
    #print("data published")



rospy.init_node('sensed_object', anonymous=False)
publisher_obj=rospy.Publisher('/turtle1/sensed_object',Pose,queue_size=1)
rospy.Subscriber('/scan', LaserScan, received_msg)

while not rospy.is_shutdown():
    #Rate set to 10Hz as given in the question 
    rate=rospy.Rate(10)
    publisher_obj.publish(pose)
    rate.sleep()