#!/usr/bin/env python 

import rospy
from geometry_msgs.msg import Twist

class iamsub():

    def __init__(self):
        rospy.init_node('/testing_g', anonymous = False)
        rospy.Subscriber('/velocity_reporter_topic', Twist, self.datagather)
        rospy.spin()

    def datagather(self, received_msg):
        self.twist = Twist()
        self.linear_vel = received_msg.linear.x
        self.angular_d = received_msg.angular.z
        rospy.loginfo("Linear velocity :- %f m/s ", self.linear_vel)
        rospy.loginfo("Angular velocity :- %f deg/s ", self.angular_d)
        rospy.loginfo(" - X - X - X - X - X - X - X - ")

if __name__ == '__main__':
    try:
        obj = iamsub()
        #obj.datagather()
    except rospy.ROSInterruptException:
        pass