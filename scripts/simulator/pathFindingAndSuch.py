#!/usr/bin/env python

from CoordinatesAndUnits import *
from sceneObjects import *

epsilon = 0.01  # 1 cm


class Route:  # find bedre navn
    noOfSteps = 0
    poses = []  # no assumptions here about speed
    travelDist = 0  # in metres will only be approximate

    def __init__(self, n, pp, td):
        self.noOfSteps = n
        self.poses = pp
        self.travelDist = td

    # Route(from, to):
    #    Route r=None
    #    r= forwardRoute(from,to)
    #    if(r==None){
    #      println("Route("+from+", "+to+") too complicated try something else!!!!!!!!!!!!!!!!")
    #      System.exit(1)
    #      noOfSteps=0 poses=None noOfSteps=0}
    #    else{noOfSteps=r.noOfSteps poses=r.poses}
    # }


def forwardRoute(fromP, to):
    travelDist = 0
    firstHalf = {}
    lastHalf = {}

    # catch infinite loops:
    pathLength = 1

    currentFrom = fromP
    currentTo = to
    while dist(currentFrom, currentTo) >= 2 * epsilon and pathLength < 100000:
        pathLength += 2
        station1 = None
        bestDist = 10000000
        for k in range(0, 101):  # use odd number (100+1) so "straight ahead" is also an option
            suggest = currentFrom.klone()
            suggest.moveRelPhiD(-maxTurn + float(k) / 101 * 2 * maxTurn, epsilon)
            suggestDist = dist(suggest, currentTo)
            if (suggestDist < bestDist):
                bestDist = suggestDist
                station1 = suggest

        firstHalf.add(station1)
        travelDist += epsilon
        currentFrom = station1
        lastHalf.add(currentTo)

        stationN = None
        bestDist = 10000000
        for k in range(0, 101):  # use odd number (100+1) so "straight ahead" is also an option
            suggest = currentTo.klone()
            suggest.moveRelPhiD(-maxTurn + float(k) / 101 * 2 * maxTurn,
                                -epsilon)  # break symmetry by change of direction
            suggestDist = dist(suggest, currentFrom)
            if (suggestDist < bestDist):
                bestDist = suggestDist
                stationN = suggest

        currentTo = stationN
        travelDist += epsilon

    allPoses = []
    for i in len(firstHalf):
        allPoses[i] = firstHalf.get(i)
    allPoses[len(firstHalf)] = avg(currentFrom, currentTo)
    travelDist = dist(fromP, to)
    for i in len(lastHalf):
        allPoses[len(firstHalf) + len(lastHalf) - i] = lastHalf[i]

    if (pathLength >= 100000):
        print("Route(" + fromP + ", " + to + ") too complicated try something else")
        sys.exit(1)
    return Route(allPoses.length, allPoses, travelDist)
    # / TEST AND MAKE A WARNING IF travelDist >> robotTurningDiameter*PI + dist(from,to)


##############################end
##############################


def backwardRoute(fromP, to):
    r = None
    r = mkBackwardRouteFromBotheEndsINTERNAL(fromP, to)
    if r == None:
        print("Route(" + fromP + ", " + to + ") too complicated try something else")
        sys.exit(1)
    return r


def mkBackwardRouteFromBotheEndsINTERNAL(fromP, to):
    r = forwardRoute(to, fromP)
    if r == None:
        return None
    # reverse
    m = r.noOfSteps / 2
    if (r.noOfSteps / 2 * 2 == r.noOfSteps):
        m += 1
    for i in m:
        p = r.poses[i]
        r.poses[i] = r.poses[r.noOfSteps - i - 2]
        r.poses[r.noOfSteps - i - 1] = p
    r.poses[r.noOfSteps - 1] = to
    return r


def forwardTurnLeftRoute(p, radius, angle):
    center = p.position.klone()
    center.moveRelXRelY(-cos(radians(p.direction)) * radius, sin(radians(p.direction)) * radius)
    phi0 = normalizeAngle(p.direction + 90)
    travelLength = radius * radians(angle)
    noOfSteps = round(travelLength / epsilon)
    poses = [noOfSteps]
    for i in noOfSteps:
        phi = normalizeAngle(phi0 - (i + 1) * angle / noOfSteps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalizeAngle(phi - 90))

    return Route(noOfSteps, poses, travelLength)


def forwardTurnRightRoute(p, radius, angle):
    center = p.position.klone()
    center.moveRelXRelY(cos(radians(p.direction)) * radius, -sin(radians(p.direction)) * radius)
    phi0 = normalizeAngle(p.direction - 90)
    travelLength = radius * radians(angle)
    noOfSteps = round(travelLength / epsilon)
    poses = [noOfSteps]
    for i in noOfSteps:
        phi = normalizeAngle(phi0 + (i + 1) * angle / noOfSteps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalizeAngle(phi + 90))

    return Route(noOfSteps, poses, travelLength)


def backwardTurnLeftRoute(p, radius, angle):
    center = p.position.klone()
    center.moveRelXRelY(-cos(radians(p.direction)) * radius, sin(radians(p.direction)) * radius)
    phi0 = normalizeAngle(p.direction + 90)
    travelLength = radius * radians(angle)
    noOfSteps = round(travelLength / epsilon)
    poses = [noOfSteps]
    for i in noOfSteps:
        phi = normalizeAngle(phi0 + (i + 1) * angle / noOfSteps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalizeAngle(phi - 90))

    return Route(noOfSteps, poses, travelLength)


def backwardTurnRightRoute(p, radius, angle):
    center = p.position.klone()
    center.moveRelXRelY(cos(radians(p.direction)) * radius, -sin(radians(p.direction)) * radius)
    phi0 = normalizeAngle(p.direction - 90)
    travelLength = radius * radians(angle)
    noOfSteps = round(travelLength / epsilon)
    poses = [noOfSteps]
    for i in noOfSteps:
        phi = normalizeAngle(phi0 - (i + 1) * angle / noOfSteps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalizeAngle(phi + 90))

    return Route(noOfSteps, poses, travelLength)
