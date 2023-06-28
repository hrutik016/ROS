#!/usr/bin/env python

#import 
import rospy
from std_msgs.msg import String
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import pow, sqrt, atan2

#class defination 
class question_2():
    
    #constant variables

    #will use this variable to store turtlebots present coordinates
    PRESENT_X = 0   
    PRESENT_Y = 0
    PRESENT_THETA = 0

    #will use this variable to store the target location where turtlebot needs to travel
    TARGET_X = 0
    TARGET_Y = 0
    TARGET_THETA = 0

    #constructor function
    def __init__(self):
        self.pose = Pose()
        self.twisttt = Twist()

        #node initialization
        rospy.init_node('pose_reporter', anonymous=False, log_level=rospy.INFO)

        #publisher1, will be used to store all the data we need to move robots in
        #next part of the question
        self.publisher_1 = rospy.Publisher('/turtle1/store', Twist, queue_size=10)

        #subscriber_1, will take in values of pose of turtle bots present coordinates
        self.subscriber_1 = rospy.Subscriber('/turtle1/pose', Pose, self.update_values)
        #subscriber_2, will take in values published by previous program(1.e it contains target coordinates)
        self.subscriber_2 = rospy.Subscriber('turtle1/destination', Pose, self.assignTarget_value)

        self.rate = rospy.Rate(2)   #2Hz, precondition given in question.

    def assignTarget_value(self, received_message):
        while not rospy.is_shutdown():
            T_for_target = Pose()
            T_for_target.x = received_message.x
            T_for_target.y = received_message.y
            self.TARGET_X = T_for_target.x
            self.TARGET_Y = T_for_target.y

    def update_values(self, received_message):
        self.pose = received_message
        self.pose.x = received_message.x
        self.pose.y = received_message.y
        self.CURRENT_X = self.pose.x
        self.CURRENT_Y = self.pose.y
        self.CURRENT_THETA = self.pose.theta
    
       
        rospy.loginfo('Pose = %s', received_message)
        self.pubs()

    def pubs(self):
        while not rospy.is_shutdown():
            self.rate = rospy.Rate(2)
            self.distance_between = sqrt(
                pow(self.TARGET_X - self.CURRENT_X, 2) + pow(self.TARGET_Y - self.CURRENT_Y, 2)
            )
            self.orientation_error = atan2(self.TARGET_X - self.TARGET_Y, self.TARGET_Y - self.CURRENT_Y)

            Store = Twist()
            Store.linear.x = self.CURRENT_X
            Store.linear.y = self.CURRENT_Y
            Store.linear.z = self.distance_between

            Store.angular.x = self.CURRENT_THETA
            Store.angular.y = self.orientation_error

            storage = Store
            self.publisher_1.publish(storage)
            self.rate.sleep()

def run_run():
    try:
        object_of_question_2 = question_2()
        rospy.spin()
    except rospy.ROSInterruptException:
        run_run()

if __name__ == '__main__':
    #while not rospy.is_shutdown():
    run_run()