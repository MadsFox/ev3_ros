#!/usr/bin/env python

from time import *
from sceneObjects import *


# keep track of all events prescribed by manuscript and make it possible for "draw" to execute it
# haha, den skal da bruge absolut tid !!!!

class Event:
    time = 0  # seconds from beginning of story
    rob = Robot
    nextPose = Pose  # in nextPose=null, self means a no-event used for implementing waiting

    def __init__(self, tt, rr, pp):
        self.time = tt
        self.rob = rr
        if isinstance(pp, Pose):
            self.nextPose = pp.klone()
        else:
            self.time = tt + pp
            self.nextPose = None
        eventList.append(self)

    def compare_to(self, event):
        d = self.time - event.time
        if d < 0:
            return -1
        elif d > 0:
            return 1
        return 0

    def to_string(self):
        return self.time + ": " + self.rob.name + self.nextPose


eventList = []


def time_of_last_generated_event(r=None):
    t = -1
    if r is not None:
        for i in eventList:
            if eventList[i].rob == r and eventList[i].time > t:
                t = eventList[i].time
    else:
        for i in eventList:
            if (i.time in eventList) < t:
                t = eventList[i].time
    return t


def sort_event_list():
    eventList.sort()


def print_event_list():
    for i in eventList:
        print(eventList[i] + "")


initialMachineTime = 0

simulationTime = 0


def init_time():
    global initialMachineTime
    initialMachineTime = clock()


def current_simulation_time():
    return (clock() - initialMachineTime) / 1000


def execute_current_events():
    t = current_simulation_time()
    # println("executeCurrentEvents() at sim. time "+t+", remaining events: " +eventList.size())
    while len(eventList) > 0 and eventList[0].time < t:
        if eventList[0].nextPose is not None:
            eventList[0].rob.pose = eventList[0].nextPose
        del eventList[0]


def no_more_events():
    return len(eventList) <= 0
