#!/usr/bin/env python

from pathFindingAndSuch import *
from eventList import *

# manuscript writing time information

mostRecentRecordedPose = []  # enough


def initial_pose(r, p):
    # maintain manuscript writing time information
    mostRecentRecordedPose[index_of(r)] = p  # crashes if robot not present
    # maintain internal reresentation of script
    Event(0, r, p)


def move_to(r, start_time, to):
    route = forward_route(mostRecentRecordedPose[index_of(r)], to)
    mostRecentRecordedPose[index_of(r)] = to
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(start_time + float(i) / 50, r, route.poses[i])


def moveTo(r, to):
    move_to(r, time_of_last_generated_event(r), to)


def moveTo(r, x, y, phi):
    move_to(r, Pose(x, y, phi))


def moveTo(r, via, to):
    move_to(r, via)
    move_to(r, to)


def moveTo(r, via1, via2, to):
    move_to(r, via1)
    move_to(r, via2)
    move_to(r, to)


def moveTo(r, via1, via2, via3, to):
    move_to(r, via1)
    move_to(r, via2)
    move_to(r, via3)
    move_to(r, to)


def moveTo(r, x1, y1, phi1, x2, y2, phi2, x, y, phi):
    move_to(r, Pose(x1, y1, phi1))
    move_to(r, Pose(x2, y2, phi2))
    move_to(r, Pose(x, y, phi))


def moveTo(r, x1, y1, phi1, x, y, phi):
    move_to(r, Pose(x1, y1, phi1))
    move_to(r, Pose(x, y, phi))


def moveToBacking(r, startTime, to):
    # returns arrival time
    route = backward_route(mostRecentRecordedPose[index_of(r)], to)
    mostRecentRecordedPose[index_of(r)] = to
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(startTime + float(i) / 50, r, route.poses[i])


def moveToBacking(r, to):
    moveToBacking(r, time_of_last_generated_event(r), to)


def moveToBacking(r, x, y, phi):
    moveToBacking(r, Pose(xx=x, yy=y, dd=phi))


def moveToBacking(r, via, to):
    moveToBacking(r, via)
    move_to(r, to)


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


def wait(r, waiting_time):
    Event(time_of_last_generated_event(r), r, waiting_time)


def circle_left(r, start_time, radius, angle=None):
    if angle is None:
        radius = start_time
        angle = radius
        start_time = time_of_last_generated_event(r)
    route = forward_turn_left_route(mostRecentRecordedPose[index_of(r)], radius, angle)
    mostRecentRecordedPose[index_of(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(start_time + float(i) / 50, r, route.poses[i])


def circle_right(r, start_time, radius, angle=None):
    if angle is None:
        radius = start_time
        angle = radius
        start_time = time_of_last_generated_event(r)
    route = forward_turn_right_route(mostRecentRecordedPose[index_of(r)], radius, angle)
    mostRecentRecordedPose[index_of(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfStepsi:
        Event(start_time + float(i) / 50, r, route.poses[i])


def circle_left_backing(r, start_time, radius, angle=None):
    if angle is None:
        radius = start_time
        angle = radius
        start_time = time_of_last_generated_event(r)
    route = backward_turn_left_route(mostRecentRecordedPose[index_of(r)], radius, angle)
    mostRecentRecordedPose[index_of(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(start_time + float(i) / 50, r, route.poses[i])


def circle_right_backing(r, start_time, radius, angle=None):
    if angle is None:
        radius = start_time
        angle = radius
        start_time = time_of_last_generated_event(r)
    route = backward_turn_right_route(mostRecentRecordedPose[index_of(r)], radius, angle)
    mostRecentRecordedPose[index_of(r)] = route.poses[route.poses.length - 1]
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(start_time + float(i) / 50, r, route.poses[i])


def synchronize():
    # all wait until slowest one up done its tasks
    synch_time = time_of_last_generated_event()
    for i in allSceneObjects:
        if isinstance(allSceneObjects[i], Robot):
            wait(allSceneObjects[i], synch_time - time_of_last_generated_event(allSceneObjects[i]))
