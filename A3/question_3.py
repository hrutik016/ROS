#!/usr/bin/env python

#import
import rospy
from std_msgs.msg import String
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import sqrt, pow, atan2

#class defination
class question_3():

    #constants
    move_x = 0 
    move_y = 0
    move_distance = 0
    move_currenttheta = 0
    move_orientation = 0

    #class constructor
    def __init__(self):
        self.pose = Pose()
        self.twisttt = Twist()

        #node initialization
        rospy.init_node("robot_driver", anonymous = False, log_level=rospy.INFO)
        
        #Subscriber_1, subscribing to the topic from previos question to take in calculation fro
        self.subscriber_1 = rospy.Subscriber('/turtle1/store', Twist, self.updating_all_values)
        
        #Publishing to Twist to cmd_vel to make the turtlebot move in turtle sim
        self.publisher_1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
        self.rate = rospy.Rate(20) #20Hz, precondiotn given in question

    #callback function of Subscriber_1
    def updating_all_values(self,received_message):
        self.twisttt = received_message
        self.twisttt.linear.x = received_message.linear.x
        self.twisttt.linear.y = received_message.linear.y
        self.twisttt.linear.z = received_message.linear.z
        self.twisttt.angular.x = received_message.angular.x
        self.twisttt.angular.y = received_message.angular.y
        self.move_x = self.twisttt.linear.x
        self.move_y = self.twisttt.linear.y
        self.move_distance = self.twisttt.linear.z
        self.move_currenttheta = self.twisttt.angular.x
        self.move_orientation = self.twisttt.angular.y
        rospy.loginfo("Present X = %s meters, Present Y = %s meters, Distance to be travelled = %s meters , Orientation of bot = %s degrees, Error Orientation = %s degrees" %(received_message.linear.x, received_message.linear.y, received_message.linear.z, received_message.angular.x, received_message.angular.y ))
        self.movement()
    
    #def target_pose(self,received_message)
        #t = Pose()
        #t.x = received_message.x
        #t.y = received_message.y
    
    #here calculating the linear velocity for bot
    def linear_vel(self,constant = 1):
        return constant * self.move_distance

    #heere calculated steering angle
    def str_angle(self):
        return self.move_orientation

    #here calculated angle 
    def angle_vel(self, constant = 1.5):
        return constant * (self.str_angle() - self.move_currenttheta)

    #movement function
    def movement(self):
        twist_movement = Twist()
        given_Tolerance = 0.01  # tolerance set to 0.01 as it was mentioned in question to have a tolerance of 10cm
        #if the condition is true, it will enter in
        while self.move_distance >= given_Tolerance:
            
            #assigning values to Twist, to move the bot
            twist_movement.linear.x = self.linear_vel()
            twist_movement.linear.y = 0
            twist_movement.linear.z = 0

            twist_movement.angular.x = 0
            twist_movement.angular.y = 0
            twist_movement.angular.z = self.angle_vel()
            #print("Here ", self.move_orientation)

            self.publisher_1.publish(twist_movement)
            self.rate.sleep()
            self.updating_all_values()

        #this is to stop the bot movement, when it reaches the target location
        twist_movement.linear.x = 0
        twist_movement.angular.z = 0
        self.publisher_1.publish(twist_movement)
        self.rate.sleep()
        
#function to run the class with its object.
def whyareyourunning():
    obj = question_3()
    rospy.spin()

if __name__ == '__main__':
    whyareyourunning()