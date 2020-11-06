#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from time import time

detik = 0
def laserScan(data):
    global detik
    print'data detik ke %s :' % detik , min(data.ranges)
    print '0 degree : '  
    print data.ranges[0]
    print '90 degree : '  
    print data.ranges[90]
    print '180 degree : '   
    print data.ranges[180]
    print '360 degree : '   
    print data.ranges[359]


    detik+=1

    
    
def read_laser_scan_data():
    rospy.Subscriber('scan',LaserScan,laserScan)

def move_motor(vel,ang):
    pub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
    move = Twist()
    move.linear.x = vel
    move.angular.z = ang
    pub.publish(move)

if __name__=='__main__':
    rospy.init_node('movement',anonymous=True)

    start_time = time()
    duration = 1 #in seconds

    forward_speed = 1
    turn_speed = 1

    while time()<start_time+duration:
        try:
            read_laser_scan_data()
            move_motor(forward_speed,turn_speed)
        except rospy.ROSInterruptException:
            pass
    else:
        move_motor(0,0)




























