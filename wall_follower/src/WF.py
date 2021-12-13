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
        self.turtle_vel = Twist()
        self.forward = (average(scan.ranges[0:18]) + average(scan.ranges[342:359])) / 2
        self.right = average(scan.ranges[265:275])
        self.right_forward = average(scan.ranges[300:310])
        self.right_behind = average(scan.ranges[230:240])
        self.pointright = scan.ranges[270]

        # angular z = rad/s -> 초당 약 57도 회전을 의미한다.

        if self.forward > 0.25:
            self.follow_wall()
        else:
            self.meet_wall()

        self.publisher.publish(self.turtle_vel)

        self.count += 1
        if self.count % 10 == 0:
            print('Forward', self.forward, '\nR:', self.right, 'fR:', self.right_forward,
                  'bR:', self.right_behind, '\npR:', self.pointright)
            print(self.count)

    def follow_wall(self):
        if self.right > 0.5 and self.right_forward > 0.5 and self.right_behind > 0.5:
            self.turtle_vel.linear.x = 0.18
            self.turtle_vel.angular.z = 0

        elif 0.18 < self.right < 0.23:
            if self.right_forward > self.right_behind:
                self.turtle_vel.linear.x = 0.15
                self.turtle_vel.angular.z = -0.3
            elif self.right_behind > self.right_forward:
                self.turtle_vel.linear.x = 0.15
                self.turtle_vel.angular.z = 0.3

        elif self.right_forward < 0.15:
            self.turtle_vel.linear.x = 0.1
            self.turtle_vel.angular.z = 0.5

        elif 0.5 < self.right_forward or self.right_forward == 0:
            self.turtle_vel.linear.x = 0.1
            self.turtle_vel.angular.z = -1.5

        else:
            self.turtle_vel.linear.x = 0.18
            self.turtle_vel.angular.z = 0


    def meet_wall(self):
        self.turtle_vel.linear.x = 0.1
        self.turtle_vel.angular.z = 2.2

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
