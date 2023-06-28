#!/usr/bin/env python


#import necessary files
import numpy as np
import rospy
from math import pow,sqrt
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D,Twist
from tf.transformations import euler_from_quaternion

#declaring variable for maintain distance from object and gap for the last bit
global maintain_dist
global gap
maintain_dist = 0.7
gap = 0.01

def Husky_sub(position):
    
    #new variable for positon
    global new_Position
    new_Position=position.pose.pose.position
    
    #variable to store orientation
    global orientt
    orientt = position.pose.pose.orientation
    orientationlist = [orientt.x , orientt.y ,orientt.z , orientt.w]
    
    #extracting roll, pitch, yaw
    global roll,pitch,yaw
    (roll,pitch,yaw)= euler_from_quaternion (orientationlist)

def Robot_movement(received_msg):
    global pose
    pose=received_msg
    
    global temp_y
    publishing = rospy.Publisher('/husky_velocity_controller/cmd_vel',Twist,queue_size=10)
    
    global movement
    movement = Twist()
    
    print('x and y running' , new_Position.x , new_Position.y)
    buff_1=maintain_dist+0.5
    buff_2=maintain_dist+0.25

    #for movement
    if pose.x>maintain_dist:
        L_Movement()
    elif pose.x<=maintain_dist:
        Rotational()
    publishing.publish(movement) 




#function for linear movement
def L_Movement():
    buff_1=maintain_dist+0.5
    buff_2=maintain_dist+0.25
    print('X and Y Coordinates are :- ' , new_Position.x , new_Position.y)
    
    global updated_x,updated_y,temp_y
     
    if pose.x<buff_1 and pose.x>=buff_2:
        updated_x=new_Position.x
        updated_y=new_Position.y
        distance=pose.x
        temp_y=yaw
        
        print(distance)
        print(updated_x , updated_y)
    
    if (pose.theta>1 and pose.x>maintain_dist):
        movement.angular.z=-0.8
        movement.linear.x=0.15
        #for right
    elif (pose.theta<-1 and pose.x>maintain_dist):
        movement.angular.z=0.8
        movement.linear.x=0.15
        #for left
    elif (pose.theta<=1 and pose.theta>=-1 and pose.x>maintain_dist):
        movement.linear.x=0.5
        movement.angular.z=0.0

#function for rotational movement
def Rotational():

    #setting value for movement 
    movement.angular.z=0.2
    movement.linear.x=0.0
    # global updated_x,updated_y

    #calculating the distance of the difference
    # distance_to_move=sqrt(pow(updated_x-(new_Position.x),2)+pow(updated_y-(new_Position.y),2))
    # dif_of_x=abs(new_Position.x)-abs(updated_x)
    # dif_of_y=abs(new_Position.y)-abs(updated_y)
    # dif_of_yaw=abs(yaw)-abs(temp_y)
    
    
    if pose.theta>88 and pose.theta<92 and pose.x<=maintain_dist:
        movement.linear.x=0.0
        movement.angular.z=0.35

        if pose.theta>95 and pose.x<maintain_dist:
            movement.linear.x=0.0
            movement.angular.z=-0.3
        if pose.theta<86 and pose.x<maintain_dist:
            movement.linear.x=0.0
            movement.angular.z=0.3
        if pose.theta>86 and pose.theta<95 and pose.x==maintain_dist:
            movement.linear.x=0.2
            movement.angular.z=0.0

    #if it reaches close to starinf point it, angular and linear velocity = 0, therefore it stops
    # if distance_to_move<0.7 and distance_to_move>0.50:
    #     movement.linear.x=0.0
    #     movement.angular.z=0.0  







def main_function():
    rospy.init_node('navigate_robot', anonymous=False)
    rospy.Subscriber('/sensed_object', Pose2D, Robot_movement)
    rospy.Subscriber('/odometry/filtered', Odometry , Husky_sub)
    rospy.spin()

if __name__ == '__main__':
    main_function()
