#!/usr/bin/env python 

import rospy
from geometry_msgs.msg import Twist

class iamsub():

    def __init__(self):
        rospy.init_node('velocity_reporter', anonymous = False)
        rospy.Subscriber('/turtle1/cmd_vel', Twist, self.datagather)
        self.publisher_obj = rospy.Publisher('/velocity_reporter_topic', Twist, queue_size=10)
        rospy.spin()

    def datagather(self, received_msg):
        #print("entering datagather ")
        self.twist = Twist()
        self.linear_vel = received_msg.linear.x
        self.angular_d = received_msg.angular.z
        self.rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            #print("in while")
            self.twist.linear.x = self.linear_vel
            self.twist.angular.z = self.angular_d
            self.publisher_obj.publish(self.twist)
            self.rate.sleep()
            #print("exiting while")  
            rospy.loginfo("Linear velocity :- %f m/s ", self.linear_vel)
            rospy.loginfo("Angular velocity :- %f rad/s ", self.angular_d)
            rospy.loginfo(" - X - X - X - X - X - X - X - ")
    
if __name__ == '__main__':
    try:
        obj = iamsub()
        #obj.datagather()
    except rospy.ROSInterruptException:
        pass


    