#!/usr/bin/env python

import numpy as np
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan

class sensor():

    Distance = 0
    Angle = 0

    def __init__(self):
        self.pose = Pose2D
        rospy.init_node("sensed_object", anonymous = False)
        self.pub = rospy.Publisher('/sensed_object', Pose2D, queue_size = 10)
        rospy.Subscriber('/scan', LaserScan, self.reader)
        
        rospy.Rate(2)
        rospy.spin()

    def reader(self, msg): 
        self.ranges = msg.ranges                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

        self.npranges = np.array(self.ranges)

        self.npranges[self.npranges > msg.range_max] = float('NaN')
        self.npranges[self.npranges < msg.range_min] = float('NaN')
        if not (np.isnan(self.npranges)).all():
            self.distance_min = np.nanmin(self.npranges)
            self.newarray = np.reshape( np.argwhere(self.npranges == self.distance_min) , -1)
            self.anglemin = ((self.newarray*msg.angle_increment)+msg.angle_min)*180.0/np.pi
        else:
            self.distance_min = float('NaN')
            self.anglemin = float('NaN')
        self.Distance = self.distance_min
        self.angle = self.anglemin
        rospy.loginfo('Min dist. [m] = %7.3f , Angles [deg] = %7.3f' , self.Distance, self.angle)
        self.publisher()


    def publisher(self):
        pose = Pose2D()
        pose.x = self.Distance
        pose.theta = self.angle
        output = pose
        
        self.pub.publish(output)
        rospy.Rate(2)

def runblock():
    try:
        obj = sensor()
                
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    runblock()
        

