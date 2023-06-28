#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Twist

#callback function from sensed object 
def dataCallback2(info_1):
    rospy.loginfo('Distance "d" from the object:- %f m', info_1.position.x)
    rospy.loginfo('Error "e" :- %f m', info_1.position.y)
    rospy.loginfo('Normalized error:- %f ', info_1.position.z)
    rospy.loginfo('x axis velocity:- %f ', info_1.orientation.x)
    rospy.loginfo('y axis velocity:- %f ', info_1.orientation.y)
    rospy.loginfo('nearest orientation from the obstacle:- %f deg', info_1.orientation.z)


#callback function from the cmdvel
def dataCallback1(info_2):
    rospy.loginfo('Linear vel %f m/s', info_2.linear.x)
    rospy.loginfo('Angular vel:- %f deg/s', info_2.linear.y)
    

def main_function():
    rospy.init_node('report_pose', anonymous=False)
    rate = rospy.Rate(2)
    rospy.Subscriber('/cmd_vel', Twist, dataCallback1)
    rospy.Subscriber('/turtle1/sensed_object', Pose, dataCallback2)
    rate.sleep()
    rospy.spin()

if __name__ == '__main__':
    main_function()