#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg  import Twist, Point
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2

x = 0.0
y = 0.0
theta = 0.0
def odom_call(msg):
    list_orientation = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    roll, pitch, theta = euler_from_quaternion(list_orientation)

    return roll, pitch , theta

def LaserBack(msg):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    rospy.Subscriber('/odometry/filtered',Odometry,odom_call)

    move=Twist()

    goal = Point ()
    goal.x = 5
    goal.y = 5

    xro = goal.x -x
    yro = goal.y -y

    angle_to_goal = atan2(xro, yro)
    if msg.ranges[180]<1:
        print msg.ranges[180]
        move.linear.x=0.0
        if abs(angle_to_goal - theta)>0.1:
        print angle_to_goal
        print theta
        move.linear.x=0.0
        move.angular.z=0.3
        else:
            print 'maju'
            move.linear.x=0.3
            move.angular.z=0.0
    else:
        print 'move to goal'
        move.linear.x=0.3
        move.angular.z=0.0
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