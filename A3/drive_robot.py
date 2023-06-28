#!/usr/bin/env python

#import

import rospy
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math


global xL, xY, theta

xL = 0
xY = 0
theta = 0

def position_robot(coordinates):
    #print("i am here @ position_robot, callback")
    global new_position
    new_position = coordinates.pose.pose.position


    global orientation_g
    orientation_g = coordinates.pose.pose.orientation
    orientation_list = [orientation_g.x , orientation_g.y ,orientation_g.z , orientation_g.w]
    
    
    global roll,pitch,yaw
    (roll,pitch,yaw)= euler_from_quaternion (orientation_list)

def robots_vel(received_msg):
    # print("i am here @ robots_vel, callback")
    global pose
    pose = received_msg
    
    publishing_obj = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    global speed
    speed = Twist()

    alpha=pose.orientation.z
    
    
    vel_x = pose.orientation.x
    vel_y = pose.orientation.y
    
    #print(vel_x, vel_y)

    dis = pose.position.x
    ee = pose.position.y
    e_mod = pose.position.z
    
    xL = new_position.x + 0.32
    yL = new_position.y
    
    Yawl = yaw

    #ratio_yx = yL / xL
    #ratio_1x = 1 / xL

    calc_1 = vel_x * math.cos(Yawl + alpha) + vel_x * (yL / xL) * (math.sin(Yawl + alpha))
    calc_2 = vel_y * (-math.sin(Yawl + alpha)) + vel_y * (yL / xL) * (math.cos (Yawl + alpha))

    now_c_1 = vel_x * (1 / xL) * (math.sin (Yawl + alpha))
    now_c_2 = vel_y * (1 / xL) * (math.cos (Yawl + alpha))

    speed.linear.x = (vel_x * (math.cos(Yawl + alpha) + (yL / xL) * (math.sin(Yawl + alpha)))) + (vel_y * (-math.sin(Yawl + alpha) + (yL / xL) * (math.cos(Yawl + alpha))) #m/s)
    speed.angular.z = now_c_1 + now_c_2
    #print("reaching here")
    print(speed.linear.x, speed.angular.z)
    publisher_obj.publish(speed)
    # print("if here it means it is getting published")
    #r.sleep()


def main_fc():
   # print("entered from main, now going to vrooooom ")
    rospy.init_node('drive_robot', anonymous=False)
    subscriber = rospy.Subscriber('/turtle1/sensed_object', Pose, robots_vel)
    subscriber_2=rospy.Subscriber('/odom',Odometry,position_robot)
    rospy.spin()

if __name__ == '__main__':
    #print("  in main function  ")
    main_fc()