#!/usr/bin/env python
# license removed for brevity
import time
import rospy
import csv
import os
from std_msgs.msg import String
from ev3_ros.msg import MotorCommands


def readInCsv():
    global robotNames
    robotNames = {}
    global filePath
    filePath = raw_input("Enter csv URI: ")
    while ".csv" not in filePath:
        print(filePath)
        filePath = raw_input("not a csv file, try again: ")

    with open(os.getcwd() + "/../data/" + filePath) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if row["name"] not in robotNames:
                robotNames[row["name"]] = {"pub": rospy.Publisher(row["name"], MotorCommands, queue_size=10),
                                           "commandDict": {round(float(row["startTime"]), 2):
                                                               {"start_time": float(row["startTime"]),
                                                                "end_time": float(row["endTime"]),
                                                                "right_speed": float(row["rightMotorSpeed"]),
                                                                "left_speed": float(row["leftMotorSpeed"])
                                                                }
                                                           }
                                           }
                print(row["name"], " has been added at: ",round(float(row["startTime"]), 2) , " with motor speeds: ", float(row["rightMotorSpeed"]))
            else:
                robotNames[row["name"]]["commandDict"][round(float(row["startTime"]), 2)] = {
                    "start_time": float(row["startTime"]),
                    "end_time": float(row["endTime"]),
                    "right_speed": float(row["rightMotorSpeed"]),
                    "left_speed": float(row["leftMotorSpeed"])
                    }
                print(row["name"], " new motor speeds at: ",round(float(row["startTime"]), 2) , " with motor speeds: ", float(row["rightMotorSpeed"]))

    return filePath


def mc_pub_csv():
    pub = rospy.Publisher('default', MotorCommands, queue_size=10)
    rospy.init_node('mc_pub_csv', anonymous=True)
    rate = rospy.Rate(100) # 10hz

    #reader = csv.DictReader(csvFile)

    mc = MotorCommands()
    mc.right_speed = 0
    mc.left_speed = 0
    rospy.loginfo(mc)

    start = raw_input("start the dance: (y/n)")
    while "y" not in start:
        if "n" in start:
            exit(0)
        start = raw_input("start the dance: (y/n)")

    start_time = time.clock()

    while not rospy.is_shutdown():
        time_diff = time.clock() - start_time

        for robot in robotNames:

            #print(" current_time: ", round(current_time,2),
            #      "robot: ", robot,
            #      " startTime: ", robotNames[robot]["commandDict"])
            if round(float(time_diff), 2) in robotNames[robot]["commandDict"]:
                #print(" startTime: ", robotNames[robot]["commandDict"],
                #      " pub: ", robotNames[robot]["pub"],
                #      " mc.right_speed: ", robotNames[robot]["commandDict"][round(current_time, 2)]["right_speed"],
                #      " mc.left_speed: ", robotNames[robot]["commandDict"][round(current_time, 2)]["left_speed"]
                #      )
                print("New speed for Robot: ", robot, "")
                pub = robotNames[robot]["pub"]
                mc.right_speed = robotNames[robot]["commandDict"][round(time_diff, 2)]["right_speed"]
                mc.left_speed = robotNames[robot]["commandDict"][round(time_diff, 2)]["left_speed"]

            rospy.loginfo(mc)
            pub.publish(mc)
            rate.sleep()


if __name__ == '__main__':
    try:
        readInCsv()
    except Exception:
        print(Exception)
        pass

    try:
        mc_pub_csv()
    except rospy.ROSInterruptException:
        pass
