#!/usr/bin/env python

from pathFindingAndSuch import *
from eventList import *

# manuscript writing time information

mostRecentRecordedPose = []  # enough


def initialPose(r, p):
    # maintain manuscript writing time information
    mostRecentRecordedPose[indexOf(r)] = p  # crashes if robot not present
    # maintain internal reresentation of script
    Event(0, r, p)


def moveTo(r, startTime, to):
    route = forwardRoute(mostRecentRecordedPose[indexOf(r)], to)
    mostRecentRecordedPose[indexOf(r)] = to
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(startTime + float(i) / 50, r, route.poses[i])


def moveTo(r, to):
    moveTo(r, timeOfLastGeneratedEvent(r), to)


def moveTo(r, x, y, phi):
    moveTo(r, Pose(xx=x, yy=y, dd=phi))


def moveTo(r, via, to):
    moveTo(r, via)
    moveTo(r, to)


def moveTo(r, via1, via2, to):
    moveTo(r, via1)
    moveTo(r, via2)
    moveTo(r, to)


def moveTo(r, via1, via2, via3, to):
    moveTo(r, via1)
    moveTo(r, via2)
    moveTo(r, via3)
    moveTo(r, to)


def moveTo(r, x1, y1, phi1, x2, y2, phi2, x, y, phi):
    moveTo(r, Pose(xx=x1, yy=y1, dd=phi1))
    moveTo(r, Pose(xx=x2, yy=y2, dd=phi2))
    moveTo(r, Pose(xx=x, yy=y, dd=phi))


def moveTo(r, x1, y1, phi1, x, y, phi):
    moveTo(r, Pose(xx=x1, yy=y1, dd=phi1))
    moveTo(r, Pose(xx=x, yy=y, dd=phi))


def moveToBacking(r, startTime, to):
    # returns arrival time
    route = backwardRoute(mostRecentRecordedPose[indexOf(r)], to)
    mostRecentRecordedPose[indexOf(r)] = to
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(startTime + float(i) / 50, r, route.poses[i])


def moveToBacking(r, to):
    moveToBacking(r, timeOfLastGeneratedEvent(r), to)


def moveToBacking(r, x, y, phi):
    moveToBacking(r, Pose(xx=x, yy=y, dd=phi))


def moveToBacking(r, via, to):
    moveToBacking(r, via)
    moveTo(r, to)


def moveToBacking(r, via1, via2, to):
    moveToBacking(r, via1)
    moveToBacking(r, via2)
    moveToBacking(r, to)


def moveToBacking(r, via1, via2, via3, to):
    moveToBacking(r, via1)
    moveToBacking(r, via2)
    moveToBacking(r, via3)
    moveToBacking(r, to)


def moveToBacking(r, x1, y1, phi1, x2, y2, phi2, x, y, phi):
    moveToBacking(r, Pose(xx=x1, yy=y1, dd=phi1))
    moveToBacking(r, Pose(xx=x2, yy=y2, dd=phi2))
    moveToBacking(r, Pose(xx=x, yy=y, dd=phi))


def moveToBacking(r, x1, y1, phi1,
                  x, y, phi):
    moveToBacking(r, Pose(xx=x1, yy=y1, dd=phi1))
    moveToBacking(r, Pose(xx=x, yy=y, dd=phi))


def wait(r, waitingTime):
    Event(timeOfLastGeneratedEvent(r), r, waitingTime)


def circleLeft(r, radius, angle):
    circleLeft(r, timeOfLastGeneratedEvent(r), radius, angle)


def circleLeft(r, startTime, radius, angle):
    route = forwardTurnLeftRoute(mostRecentRecordedPose[indexOf(r)], radius, angle)
    mostRecentRecordedPose[indexOf(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(startTime + float(i) / 50, r, route.poses[i])


def circleRight(r, radius, angle):
    circleRight(r, timeOfLastGeneratedEvent(r), radius, angle)


def circleRight(r, startTime, radius, angle):
    route = forwardTurnRightRoute(mostRecentRecordedPose[indexOf(r)], radius, angle)
    mostRecentRecordedPose[indexOf(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfStepsi:
        Event(startTime + float(i) / 50, r, route.poses[i])


def circleLeftBacking(r, radius, angle):
    circleLeftBacking(r, timeOfLastGeneratedEvent(r), radius, angle)


def circleLeftBacking(r, startTime, radius, angle):
    route = backwardTurnLeftRoute(mostRecentRecordedPose[indexOf(r)], radius, angle)
    mostRecentRecordedPose[indexOf(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(startTime + float(i) / 50, r, route.poses[i])


def circleRightBacking(r, radius, angle):
    circleRightBacking(r, timeOfLastGeneratedEvent(r), radius, angle)


def circleRightBacking(r, startTime, radius, angle):
    route = backwardTurnRightRoute(mostRecentRecordedPose[indexOf(r)], radius, angle)
    mostRecentRecordedPose[indexOf(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(startTime + float(i) / 50, r, route.poses[i])


def synchronize():
    # all wait until slowest one up done its tasks
    synchTime = timeOfLastGeneratedEvent()
    for i in allSceneObjects:
        if isinstance(allSceneObjects[i], Robot):
            wait(allSceneObjects[i], synchTime - timeOfLastGeneratedEvent(allSceneObjects[i]))


def synchronize(r1, r2):
    # !!!!!!!! VERY LAZY - NOT IMPLEMENTED WORKS ONLY FOR AN EXAMPLE WITH AXACTLY TWO ROBOTS ON STAGE!!!
    # all wait until slowest one up done its tasks
    synchTime = timeOfLastGeneratedEvent()
    for i in allSceneObjects:
        if isinstance(allSceneObjects[i], Robot):
            wait(allSceneObjects[i], synchTime - timeOfLastGeneratedEvent(allSceneObjects[i]))
