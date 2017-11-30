#!/usr/bin/env python
# license removed for brevity
import rospy
import csv
from std_msgs.msg import String
from ev3_ros.msg import MotorCommands

def readInCsv():
    filePath = raw_input("Enter csv URI: ")
    csvInFile = ".csv" in filePath
    while not csvInFile:
        print(filePath)
        filePath = raw_input("not a csv file, try again: ")
        csvInFile = ".csv" in filePath
    with open(filePath) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            print(row["startTime"], row["name"])

def mc_pub_csv():
    pub = rospy.Publisher('Frederik', MotorCommands, queue_size=10)
    rospy.init_node('mc_pub_csv', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    mc = MotorCommands()
    mc.right_speed = 10.10
    mc.left_speed = 5.5
    while not rospy.is_shutdown():

        rospy.loginfo(mc)
        pub.publish(mc)
        rate.sleep()

if __name__ == '__main__':
    #try:
    readInCsv()
    #except Exception:
    #    print(Exception)
    #    pass

    try:
        mc_pub_csv()
    except rospy.ROSInterruptException:
        pass
