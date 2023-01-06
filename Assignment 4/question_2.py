#!/usr/bin/env python

#importing th required libraries
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
    
    
    global roll, pitch, yaw
    (roll,pitch,yaw)= euler_from_quaternion (orientation_list)

def robots_vel(received_msg):
    # print("i am here @ robots_vel, callback")
    global pose
    pose = received_msg
    
    publishing_obj = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    global move
    #making a Twist object to store 
    move = Twist()

    alpha=pose.orientation.z
    
    #distance, 
    dis = pose.position.x
    ee = pose.position.y
    e_mod = pose.position.z
    
    xL = new_position.x + 0.25
    yL = new_position.y
    
    #velocity of x and y  
    vel_x = pose.orientation.x
    vel_y = pose.orientation.y
    
    #print(vel_x, vel_y)
    
    Yawl = yaw

    ratio_yx = yL / xL
    ratio_1x = 1 / xL

    calc_1 = vel_x * math.cos(Yawl + alpha) + vel_x * (ratio_yx) * (math.sin(Yawl + alpha))
    calc_2 = vel_y * (-math.sin(Yawl + alpha)) + vel_y * (ratio_yx) * (math.cos (Yawl + alpha))

    now_c_1 = vel_x * (ratio_1x) * (math.sin (Yawl + alpha))
    now_c_2 = vel_y * (ratio_1x) * (math.cos (Yawl + alpha))

    move.linear.x = (vel_x * (math.cos(Yawl + alpha) + (ratio_yx) * (math.sin(Yawl + alpha)))) + (vel_y * (-math.sin(Yawl + alpha) + (ratio_yx) * (math.cos(Yawl + alpha)))) #m/s)
    #move.angular.z = now_c_1 + now_c_2
    move.angular.z = vel_x * ((ratio_1x) * (math.sin (Yawl + alpha))) + vel_y * ((ratio_1x) * (math.cos (Yawl + alpha)))

    #print("reaching here")
    print(move.linear.x, move.angular.z)
    publishing_obj.publish(move)
    # print("if here it means it is getting published")
    #r.sleep()


def main_fc():
   # print("entered from main, now going to vrooooom ")
    rospy.init_node('drive_robot', anonymous=False)
    subscriber = rospy.Subscriber('/turtle1/sensed_object', Pose, robots_vel)
    subscriber_2=rospy.Subscriber('/odom',Odometry, position_robot)
    rospy.spin()

if __name__ == '__main__':
    #print("  in main function  ")
    #while not rospy.is_shutdown():
    main_fc()