#!/usr/bin/env python
# license removed for brevity
import rospy
from ev3_ros.msg import MotorCommands


def mc_pub_test():
    pub = rospy.Publisher('default', MotorCommands, queue_size=10)
    rospy.init_node('mc_pub_csv', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    mc = MotorCommands()

    while not rospy.is_shutdown():
        mc.right_speed = float(raw_input("right motor speed: "))
        mc.left_speed = float(raw_input("left motor speed: "))

        for i in range(0, 20):
            rospy.loginfo(mc)
            pub.publish(mc)
            rate.sleep()


if __name__ == '__main__':

    try:
        mc_pub_test()
    except rospy.ROSInterruptException:
        pass
