#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from myturtle.msg import landmark_distance




def jarak(x1,y1,x2,y2):
	xd=x1-x2
	yd=y1-y2
	return math.sqrt(abs(xd*xd - yd*yd))

class landmark_monitor(object):
	def __init__(self,pub, benda):
		self._pub=pub
		self._benda=benda

	def callback(self, msg):
		x=msg.pose.pose.position.x
		y=msg.pose.pose.position.y
		closest_name=None
		closest_dist=None
		for lname,lx,ly in self._benda:
			dist= jarak(x, y, lx, ly)
			if closest_dist is None or dist < closest_dist:
				closest_name=lname
				closest_dist=dist
		ld =landmark_distance()
		ld.name=closest_name
		ld.distance=closest_dist
		self._pub.publish(ld)
		if closest_dist < 0.5:
			rospy.loginfo('Dekat:{}'.format(closest_name))


def main():
	rospy.init_node('location_monitor')
	
	benda=[]
	benda.append(('Cube', 0.31,-0.99));
	benda.append(('Dumpster', 0.11,-2.42));
	benda.append(('Cylinder', -1.14,-2.88));
	benda.append(('Barrier', -2.59,-0.83));
	benda.append(('Bookshelf', -0.09,0.53));
	
	pub=rospy.Publisher('closest_benda', landmark_distance, queue_size=10)
	monitor = landmark_monitor(pub, benda)
	rospy.Subscriber('/odom', Odometry, monitor.callback)	
	rospy.spin()


if __name__=='__main__':
	main()
