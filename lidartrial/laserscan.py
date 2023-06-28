#!/usr/bin/env python

import numpy as np
import rospy 
from sensor_msgs.msg import LaserScan

def callback(msg):
    ranges = msg.ranges

    npranges = np.array(ranges)

    npranges[npranges > msg.range_max] = float('NaN')
    npranges[npranges < msg.range_min] = float('Nan')

    min_distance = np.nanmin(npranges)
    indices = np.reshape(np.argwhere(npranges == min.distance), -1)

    rospy.loginfo('Min dist. [m] = %7.3f, Angles [deg] = %7.3f', min_distance, ((indices * msg.angle_increment) + msg.angle_min) * 180.0 / np.pi)

def laser_scan_reader():
    rospy.init_node('laser_scan_reader', anonymous=False)
    rospy.Subscriber('/scan', LaserScan, callback)
    rospy.spin()


if __name__ == '__main__':
    laser_scan_reader()