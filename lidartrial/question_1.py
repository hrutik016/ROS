#!/usr/bin/env python

#import necessary
import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Pose2D


global dist_x, theta
pose=Pose2D()

def callback(received_msg):
    global pose
    ranges = received_msg.ranges

    # converting it to numpy array to be able to use numpy functions
    npranges = np.array(ranges)

    # converting the values out of range to 'NaN' to be ignored in calculation
    npranges[npranges > received_msg.range_max] = float('NaN')
    npranges[npranges < received_msg.range_min] = float('NaN')


    if not (np.isnan(npranges)).all():
        # compute minimum distance and i
        min_distance = np.nanmin(npranges)
        indices = np.reshape( np.argwhere(npranges == min_distance) , -1)
        min_angle = float(((indices * received_msg.angle_increment) + received_msg.angle_min) * 180.0/np.pi)
    else:
        #for the time when the object is not sensed
        min_distance = float('NaN')
        min_angle = float('NaN')
    
    pose.x=min_distance
    pose.theta=min_angle
    print( pose.x , pose.theta)
    publishing.publish(pose)

rospy.init_node('sensed_object', anonymous=False)
publishing = rospy.Publisher('/sensed_object',Pose2D,queue_size=1)
rospy.Subscriber('/scan', LaserScan, callback)

while not rospy.is_shutdown():
    rate=rospy.Rate(2)
    publishing.publish(pose)
    rate.sleep()