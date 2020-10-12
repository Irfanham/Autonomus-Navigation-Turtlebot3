#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry


benda=[]
benda.append(('Cube', 0.31,-0.99));
benda.append(('Dumpster', 0.11,-2.42));
benda.append(('Cylinder', -1.14,-2.88));
benda.append(('Barrier', -2.59,-0.83));
benda.append(('Bookshelf', -0.09,0.53));

def jarak(x1,y1,x2,y2):
	xd=x1-x2
	yd=y1-y2
	return math.sqrt(abs(xd*xd - yd*yd))


def callback(msg):
	x=msg.pose.pose.position.x
	y=msg.pose.pose.position.y
	closest_name=None
	closest_dist=None
	for lname,lx,ly in benda:
		dist= jarak(x, y, lx, ly)
		if closest_dist is None or dist < closest_dist:
			closest_name=lname
			closest_dist=dist
	rospy.loginfo('closest: {}'.format(closest_name))


def main():
	rospy.init_node('location_monitor')
	rospy.Subscriber('/odom', Odometry, callback)	
	rospy.spin()


if __name__=='__main__':
	main()
