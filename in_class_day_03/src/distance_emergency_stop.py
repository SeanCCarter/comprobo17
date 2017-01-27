#!/usr/bin/env python

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import rospy

class distanceEStopNode(object):
  def __init__(self):
    rospy.init_node('emergencyStop')
    self.r = rospy.Rate(5)
    rospy.Subscriber('/scan', LaserScan, self.process_scan)
    self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    self.sees_obstacle = False

  def process_scan(self, m):
  	self.sees_obstacle = False
  	for distance in m.ranges:
  		if distance < .5 and distance != 0.0:
  			self.sees_obstacle = True

  def run(self):
    go_command = Twist()
    go_command.linear.x = .1
    stop_command = Twist()
    stop_command.linear.x = 0
    while not rospy.is_shutdown():
      if self.sees_obstacle:
        self.publisher.publish(stop_command)
      else:
        self.publisher.publish(go_command)
      self.r.sleep()

if __name__ == '__main__':
  node = distanceEStopNode()
  node.run()