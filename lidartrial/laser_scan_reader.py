#!/usr/bin/env python

## Subscribes to topic /scan of type LaserScan and display the minimum
## distance to an obstacle and their angle(s) relative to the scanner's
## reference frame

import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Pose2D


global distance,theta
pose=Pose2D()

def callback(received_msg):
    global pose
    ranges = received_msg.ranges

    # convert to numpy array to be able to use numpy functions
    npranges = np.array(ranges)

    # convert values out of range to 'NaN' to be ignored in calculation
    npranges[npranges > received_msg.range_max] = float('NaN')
    npranges[npranges < received_msg.range_min] = float('NaN')

    # compute minimum distance and its corresponding angles with respect to scanner's frame
    min_distance = np.nanmin(npranges)
    indices = np.reshape( np.argwhere(npranges == min_distance) , -1)

    rospy.loginfo('Minimum distance [m] = %7.3f , Angle [deg] = %7.3f', min_distance, ((indices*received_msg.angle_increment)+received_msg.angle_min)*180.0/np.pi)
    pose.distance=min_distance
    pose.theta=float(((indices*msg.angle_increment)+msg.angle_min)*180.0/np.pi)
    print( pose.distance , pose.theta)
    pub.publish(pose)

rospy.init_node('sensed_object', anonymous=False)
pub=rospy.Publisher('/location',Pose2D,queue_size=1)
rospy.Subscriber('/scan', LaserScan, callback)

while not rospy.is_shutdown():
    rate=rospy.Rate(2)
    pub.publish(pose)
    rate.sleep()