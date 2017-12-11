#!/usr/bin/env python

from time import *
from CoordinatesAndUnits import *
from sceneObjects import *


# keep track of all events prescribed by manuscript and make it possible for "draw" to execute it
# haha, den skal da bruge absolut tid !!!!

class Event:
    time = 0  # seconds from beginning of story
    rob = Robot
    nextPose = Pose  # in nextPose=null, self means a no-event used for implementing waiting

    def __init__(self, tt, rr, *args, **kwargs):
        self.time = tt
        self.rob = rr
        if "pp" in kwargs:
            self.nextPose = kwargs.get("pp").klone()
        elif "waitingTime" in kwargs:
            self.time = tt + kwargs.get("waitingTime")
            self.nextPose = None
        eventList.add(self)

    def compareTo(self, e):
        d = self.time - e.time
        if d < 0:
            return -1
        elif d > 0:
            return 1
        return 0

    def toString(self):
        return self.time + ": " + self.rob.name + self.nextPose


eventList = []


def timeOfLastGeneratedEvent():
    t = -1
    for i in eventList:
        if (i.time in eventList) < t:
            t = eventList[i].time
    return t


def timeOfLastGeneratedEvent(r):
    t = -1
    for i in eventList:
        if eventList[i].rob == r and eventList[i].time > t:
            t = eventList[i].time
    return t


def sortEventList():
    eventList.sort()


def printEventList():
    for i in eventList:
        print(eventList[i] + "")


initialMachineTime = 0

simulationTime = 0


def initTime():
    initialMachineTime = time.clock()


def currentSimulationTime():
    return (time.clock() - initialMachineTime) / 1000


def executeCurrentEvents():
    t = currentSimulationTime()
    # println("executeCurrentEvents() at sim. time "+t+", remaining events: " +eventList.size())
    while len(eventList) > 0 and eventList[0].time < t:
        if eventList[0].nextPose is not None:
            eventList[0].rob.pose = eventList[0].nextPose
        del eventList[0]


def noMoreEvents():
    return eventList.isEmpty()

