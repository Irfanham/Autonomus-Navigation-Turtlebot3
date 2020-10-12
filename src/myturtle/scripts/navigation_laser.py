#!/usr/bin/env python
import rospy
import sensor_msgs.msg
import random
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from itertools import *
from operator import itemgetter 

x = 0.0 #forward linear velocity
TH = 1.5 #threshold value for laser
PI = 3.14 #phi
Kp = 0.05 #koefisien proporsional
z = 0

def laserScan(data):
	range_angles = np.arange(len(data.ranges))
	ranges =  np.array(data.ranges)
	range_mask = (ranges > TH)
	ranges = list(range_angles[range_mask])
	max_gap = 40

	gap_list = []
	for k, g in groupby(enumerate(ranges), lambda(i,x):i-x):
		gap_list.append(map(itemgetter(1), g))
	gap_list.sort(key=len)
	largest_gap = gap_list[-1]
	min_angle, max_angle = largest_gap[0]*((data.angle_increment)*180/PI), largest_gap[-1]*((data.angle_increment)*180/PI)

	avg_gap = (max_angle - min_angle)/2

	turn_angle = min_angle + avg_gap

	print(min_angle, max_angle)
	print(max_gap, avg_gap, turn_angle)

	global x
	global z
	if avg_gap < max_gap:
		z = -0.5
	else:
		x = 0.5
		z = Kp*(-1)*(90 - turn_angle)

def main():
	rospy.init_node('scan_listener', anonymous=True) #initialize node
	
	pub=rospy.Publisher('/cmd_vel',Twist, queue_size=10) #publisher
	
	rospy.Subscriber("scan",sensor_msgs.msg.LaserScan,laserScan) #subscriber

	rate = rospy.Rate(10) #10hz

	while not rospy.is_shutdown():
		command = Twist()
		command.linear.x = x
		command.angular.z = z
		current_time = rospy.Time.now()
		pub.publish(command)
		rate.sleep()

if __name__=='__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass

	
