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

        # angular z = rad/s -> 초당 약 57도 회전을 의미한다.
        turtle_vel.linear.x = 0.18
        turtle_vel.angular.z = 0

        if 0.2 < right < 0.25:
            if right_forward > right_behind:
               turtle_vel.linear.x = 0.15
               turtle_vel.angular.z = -0.3
            elif right_behind > right_forward:
               turtle_vel.linear.x = 0.15
               turtle_vel.angular.z = 0.3

        elif right_forward > 0.5 or right_forward == 0:
            turtle_vel.linear.x = 0.1
            turtle_vel.angular.z = -1

        self.publisher.publish(turtle_vel)

        self.count += 1
        if self.count % 10 == 0:
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
