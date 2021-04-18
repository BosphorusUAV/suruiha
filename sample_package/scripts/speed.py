#!/usr/bin/env python

import sys

import rospy
from mav_msgs.msg import Actuators


def set_speed(uav_id=1):
    print("uav_id:", uav_id, "initialized")
    pub = rospy.Publisher('command/motor_speed', Actuators, queue_size=10)
    rospy.init_node('speed', anonymous=True)
    rate = rospy.Rate(10)

    
    speed = Actuators()

    while not rospy.is_shutdown():
        speed.header.stamp = rospy.Time.now()
        speed.header.seq += 1
        
        if speed.header.seq < 10:
            # iha'nin pervane hizlari
            speed.angular_velocities = [3000, 3000, 3000, 3000]
        else:
            speed.angular_velocities = [1500, 1500, 1500, 1500]
        
        pub.publish(speed)
        
        rate.sleep()

if __name__ == '__main__':
    rospy.sleep(6)
    set_speed(sys.argv[1])