#!/home/pi/.pyenv/versions/rospy385/bin/python

import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class WallFollower:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 0

    def lds_callback(self, scan):
        turtle_vel = Twist()
        forward = (average(scan.ranges[0:18]) + average(scan.ranges[342:359])) / 2
        right = average(scan.ranges[265:275])
        right_forward = average(scan.ranges[300:310])
        right_behind = average(scan.ranges[230:240])
        pointright = scan.ranges[270]
        self.count += 1
        print('Forward', forward, '\nR:', right, 'fR:', right_forward,
              'bR:', right_behind, '\npR:', pointright)
        print(self.count)



def average(some_list):
    return sum(some_list)/len(some_list)


def main():
    rospy.init_node('wall_follwer')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = WallFollower(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()
