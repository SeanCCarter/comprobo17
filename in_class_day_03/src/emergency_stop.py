#!/usr/bin/env python

from neato_node.msg import Bump
from geometry_msgs.msg import Twist
import rospy

class eStopNode(object):
  def __init__(self):
    rospy.init_node('emergencyStop')
    self.r = rospy.Rate(5)
    rospy.Subscriber('/bump', Bump, self.process_bump)
    self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    self.has_bumped = False

  def process_bump(self, m):
    if m.leftFront or m.leftSide or m.rightFront or m.rightSide:
      self.has_bumped = True
    else:
      self.has_bumped = False

  def run(self):
    go_command = Twist()
    go_command.linear.x = .1
    stop_command = Twist()
    stop_command.linear.x = 0
    while not rospy.is_shutdown():
      if self.has_bumped:
        self.publisher.publish(stop_command)
      else:
        self.publisher.publish(go_command)
      self.r.sleep()

if __name__ == '__main__':
  node = eStopNode()
  node.run()