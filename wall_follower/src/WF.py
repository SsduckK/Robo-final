#!/home/pi/.pyenv/versions/rospy385/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class WallFollower:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        pass


def main():
    rospy.init_node('wall_follwer')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = WallFollower(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()
