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
                print(row["name"] + " has been added")
            else:
                robotNames[row["name"]]["commandDict"] = {round(float(row["startTime"]), 2):
                                                              {"start_time": float(row["startTime"]),
                                                               "end_time": float(row["endTime"]),
                                                               "right_speed": float(row["rightMotorSpeed"]),
                                                               "left_speed": float(row["leftMotorSpeed"])
                                                               }
                                                          }

    return filePath

def mc_pub_csv(file):
    pub = rospy.Publisher('default', MotorCommands, queue_size=10)
    rospy.init_node('mc_pub_csv', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    #reader = csv.DictReader(csvFile)

    mc = MotorCommands()
    mc.right_speed = 0
    mc.left_speed = 0
    rospy.loginfo(mc)

    print(file)

    start = raw_input("start the dance: (y/n)")
    while "y" not in start:
        if "n" in start:
            exit(0)
        start = raw_input("start the dance: (y/n)")

    start_time = time.clock()

    while not rospy.is_shutdown():
        for robot in robotNames:

            current_time = time.clock() - start_time

            print(" current_time: ", round(current_time,2),
                  "robot: ", robot)
            if round(current_time,2) in robotNames[robot]["commandDict"]:
                print("file is here")
                print(" startTime: ", robotNames[robot]["commandDict"][round(current_time,2)]["startTime"],
                        #" endTime: ", robot["commandDict"][current_time]["endTime"],
                        #" right_speed: ", robot["commandDict"][current_time]["right_speed"],
                        #" left_speed: ", robot["commandDict"][current_time]["left_speed"],
                        )

            #if row["startTime"] < current_time and current_time < row["endTime"] and rospy.is_running():
            #    current_time = time.clock() - start_time
            #    pub = robotNames[row["name"]]
            #    mc.right_speed = row["rightMotorSpeed"]
            #    mc.left_speed = row["leftMotorSpeed"]
            #
            #    prevRow = row
            #    prevRow1 = prevRow
            #    prevRow2 = prevRow1
            #
            #rospy.loginfo(mc)
            #pub.publish(mc)
            #rate.sleep()

if __name__ == '__main__':
    try:
        fp = readInCsv()
    except Exception:
        print(Exception)
        pass

    try:
        mc_pub_csv(fp)
    except rospy.ROSInterruptException:
        pass
