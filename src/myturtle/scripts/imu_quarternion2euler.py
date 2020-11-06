#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
import math

def quaternion_to_euler_angle(msg):
	x = msg.x
	y = msg.y
	z = msg.z
	w = msg.w

	ysqr = y * y
	
	t0 = +2.0 * (w * x + y * z)
	t1 = +1.0 - 2.0 * (x * x + ysqr)
	X = math.degrees(math.atan2(t0, t1))
	
	t2 = +2.0 * (w * y - z * x)
	t2 = +1.0 if t2 > +1.0 else t2
	t2 = -1.0 if t2 < -1.0 else t2
	Y = math.degrees(math.asin(t2))
	
	t3 = +2.0 * (w * z + x * y)
	t4 = +1.0 - 2.0 * (ysqr + z * z)
	Z = math.degrees(math.atan2(t3, t4))
	
	return X, Y, Z

def callback(msg):
	X, Y, Z = quaternion_to_euler_angle(msg.orientation)
	print "Quaternoion ================"
	print "x : ", msg.orientation.x
	print "y : ", msg.orientation.y
	print "z : ", msg.orientation.z
	print "w : ", msg.orientation.w
	print "Euler -----------------------"
	print "X : ", X
	print "Y : ", Y
	print "Z : ", Z

rospy.init_node('get_imu_data')

sub = rospy.Subscriber('imu', Imu, callback)

rospy.spin()