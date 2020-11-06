#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg  import Twist, Point
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2


def LaserBack(msg):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
   
    move=Twist()
    threshold = 1
    print msg.ranges[180]
    if  msg.ranges[180]<threshold:       
        move.linear.x=0.0
        move.angular.z=0.5
    else:
        move.linear.x=0.5
        move.angular.z=0.0
        if  msg.ranges[180]<threshold :       
            move.linear.x=0.0
            move.angular.z=0.5
            
    pub.publish(move)
    

def main():
    rospy.init_node('check_obstacle', anonymous=True)
    rospy.Subscriber('/scan',LaserScan,LaserBack)
        
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass