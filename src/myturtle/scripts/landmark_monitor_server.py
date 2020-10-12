#!/usr/bin/env python

import math
import rospy

from myturtle.srv import *
from nav_msgs.msg import Odometry

class LandmarkMonitor(object):
	def __init__(self):
		self._benda = {
			"Cube":(0.31,-0.99),
			"Dumpster":(0.11,-2.42),
			"Cylinder":(-1.14,-2.88),
			"Barrier":(-2.59,-0.83),
			"Bookshelf":(-0.09,0.53)
		}
		self._x = 0
		self._y = 0


	def get_closest(self, req):
		rospy.loginfo('GetClosest called')
		best_landmark= ''
		best_distance=-1
		for name, (x, y) in self._benda.items():
			dx = x - self._x
			dy = y - self._y
			sq_dist = dx*dx + dy*dy
			if best_distance == -1 or sq_dist < best_distance:
				best_distance = sq_dist
				best_landmark = name
		response = GetClosestResponse()
		response.name = best_landmark
		return response	
	
	def get_distance(self, req):
		rospy.loginfo('GetDistance called with {}'.format(req.name))
		if req.name not in self._benda:
			rospy.logerr('Tidak dikenali "{}"'.format(req.name))
			return None
		x, y = self._benda[req.name]
		dx = x - self._x
		dy = y - self._y
		response = GetDistanceResponse()
		response.distance = math.sqrt(abs(dx*dx+dy*dy))
		return response
	def odom_callback(self, msg):
		self._x = msg.pose.pose.position.x
		self._y = msg.pose.pose.position.y
		
  

def main():
	rospy.init_node('landmark_server')
	monitor = LandmarkMonitor()
	get_closest = rospy.Service('get_closest', GetClosest, monitor.get_closest)
	get_distance = rospy.Service('get_distance', GetDistance, monitor.get_distance)
	sub = rospy.Subscriber('/odom', Odometry, monitor.odom_callback)
	rospy.spin()	



if __name__=='__main__':
	main()
