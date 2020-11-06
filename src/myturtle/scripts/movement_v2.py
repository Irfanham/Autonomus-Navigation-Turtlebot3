#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist,Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from time import time
from tf.transformations import euler_from_quaternion
from math import atan2

x = 0.0
y = 0.0
theta = 0.0


#move robot to goal
def move_toGoal(msg):
        global x
        global y
        global theta

        x = msg.pose.pose.position.x #position x
        y = msg.pose.pose.position.y #position y
        ori = msg.pose.pose.orientation
        (roll, picth, theta) = euler_from_quaternion([ori.x, ori.y,ori.z,ori.w])
    
rospy.init_node('speed_contoller')
sub = rospy.Subscriber("/odometry/filtered", Odometry, move_toGoal)
pub = rospy.Publisher("/cmd_vel", Twist,queue_size = 1)

speed = Twist()

rate = rospy.Rate(4)
goal = Point()

goal.x = 5
goal.y = 5

while  not rospy.is_shutdown:  
        inc_x = goal.x -x
        inc_y = goal.y -y

        gTheta = atan2(inc_x, inc_y)

        if abs (gTheta - theta)>0.1:
                speed.linear.x = 0.0
                speed.angular.z = 0.3
        else:
                speed.linear.x = 0.5
                speed.angular.z = 0.0
        pub.publish(speed)        
        rate.sleep()
