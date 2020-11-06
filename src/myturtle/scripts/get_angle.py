#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from math import sqrt, pow, pi, atan2
from tf.transformations import euler_from_quaternion
import numpy as np


x = 0.0
y = 0.0
theta = 0.0


def pos_callback(msg):
    global x,y,theta
    
    x = msg.pose.pose.position.x #position x
    y = msg.pose.pose.position.y #position y
    orientation = msg.pose.pose.orientation
        
    (roll, picth, theta) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])

    return x, y, theta

def main():
    rospy.init_node('get_angle', anonymous=True)
    rospy.Subscriber('/odometry/filtered',Odometry, pos_callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    move = Twist()
    rate = rospy.Rate(5)
    print("goal_x = ")
    goal_x = input()
    print("goal_y = ")
    goal_y = input()
    # print(" goal_z = ")
    # goal_z = input()

    goal = Point()
    goal.x = goal_x
    goal.y = goal_y
    # goal.z = goal_z

    
    print"go"
    inc_x = goal.x -x
    inc_y = goal.y -y

    gTheta = atan2(inc_x, inc_y)

    if abs (gTheta - theta)>0.1:
        move.linear.x = 0.0
        move.angular.z = 0.5
    else:
        move.linear.x = 0.5
        move.angular.z = 0.0
    pub.publish(move)        
    
    rate.sleep()
        
    rospy.spin()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
