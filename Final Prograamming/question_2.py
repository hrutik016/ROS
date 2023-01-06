#!/usr/bin/env python 

import rospy 
from geometry_msgs.msg import Twist
import math 

#initializing the class
class move_backward():
    def __init__(self):
        self.twist = Twist()
        rospy.init_node('drive_negative_v_w', anonymous = False)
        self.publisher_obj = rospy.Publisher('turtle1/cmd_vel',  Twist, queue_size=1)

    def for_publisher_func(self):       
        self.rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.twist.linear.x = -0.5
            self.twist.angular.z = -0.5
            self.publisher_obj.publish(self.twist)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        obj = move_backward()
        obj.for_publisher_func()
    except rospy.ROSInterruptException:
        pass
