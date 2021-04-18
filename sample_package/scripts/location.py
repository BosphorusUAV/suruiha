#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

location = None

def callback(data):
    global location
    location = data.pose.pose.position
    # print("location info:", location)

def get_location():
    rospy.init_node('location', anonymous=True)
    rospy.Subscriber('odometry', Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    get_location()