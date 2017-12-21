#!/usr/bin/env python

from pathFindingAndSuch import *
from eventList import *

# manuscript writing time information

mostRecentRecordedPose = []  # enough


def initial_pose(r, po):
    # maintain manuscript writing time information
    mostRecentRecordedPose[index_of(r)] = p  # crashes if robot not present
    # maintain internal reresentation of script
    Event(0, r, po)


def moveTo(r, *args):
    start_time = time_of_last_generated_event(r)
    r_index = allSceneObjects.index(r)
    rob = allSceneObjects[r_index]
    to = args[0]
    if len(args) is 2 and not isinstance(Pose, args[0]):
        start_time = args[0]
        to = args[1]
    elif len(args) > 2 and not isinstance(Pose, args[0]):
        moveTo(r, Pose(args[0], args[1], args[2]), args[3:])
    elif len(args) > 2:
        to = args[0]
        moveTo(r, args[1:])
    route = forward_route(mostRecentRecordedPose[index_of(r)], to, rob.max_turn)
    mostRecentRecordedPose[index_of(r)] = to
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(start_time + float(i) / 50, r, route.poses[i])


def moveToBacking(r, *args):
    start_time = time_of_last_generated_event(r)
    r_index = allSceneObjects.index(r)
    rob = allSceneObjects[r_index]
    to = args[0]
    if len(args) is 2 and not isinstance(Pose, args[0]):
        start_time = args[0]
        to = args[1]
    elif len(args) > 2 and not isinstance(Pose, args[0]):
        moveToBacking(r, Pose(args[0], args[1], args[2]), args[3:])
    elif len(args) > 2:
        to = args[0]
        moveToBacking(r, args[1:])
    route = backward_route(mostRecentRecordedPose[index_of(r)], to, rob.max_turn)
    mostRecentRecordedPose[index_of(r)] = to
    # arbitrary speed in this version
    for i in route.noOfSteps:
        Event(start_time + float(i) / 50, r, route.poses[i])


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
