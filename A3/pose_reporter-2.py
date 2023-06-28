#!/usr/bin/env python

## Subscribes to turtlesim/Pose published on topic '/turtle1/pose'

import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist


def callback(data1):
    rospy.loginfo('distance from obstacle = %f', data1.position.x)
    rospy.loginfo('distance tracking error = %f', data1.position.y)
    rospy.loginfo('distance normalised error = %f', data1.position.z)
    rospy.loginfo('velocity x axis = %f', data1.orientation.x)
    rospy.loginfo('velocity y axis = %f', data1.orientation.y)
    rospy.loginfo('nearest orientation from obstacle = %f', data1.orientation.z)

def callback1(data2):
    rospy.loginfo('distance from obstacle = %f', data2.linear.x)
    rospy.loginfo('distance tracking error = %f', data2.angular.z)

def listener():
    rospy.init_node('report_pose', anonymous=False)

    rospy.Subscriber('/cmd_vel', Twist, callback1)
    rospy.Subscriber('/turtle1/sensed_object', Pose, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
