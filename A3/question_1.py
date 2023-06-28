#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class my_publisher:

    def __init__(self):
        self.pose = Pose()
        self.pub_obj = rospy.Publisher('/turtle1/destination', Pose, queue_size=10)
        rospy.init_node('target_publisher', anonymous=False)
    
        

    def user_input(self):
        target_pose = Pose()
        target_pose.x = float(input("Enter x coordinate: "))
        target_pose.y = float(input("Enter y coordinate: "))
        if(target_pose.x <= 11 and target_pose.x >= 0) and (target_pose.y <= 11 and target_pose.y >= 0):
            rate = rospy.Rate(10)
            while not rospy.is_shutdown():
                sensor_output_str = target_pose
                rospy.loginfo(sensor_output_str)
                self.pub_obj.publish(sensor_output_str)
                rate.sleep()
        else:
            user_input()

def run():
    obj = my_publisher()
    obj.user_input()   

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass