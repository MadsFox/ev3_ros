#!/usr/bin/env python

from CoordinatesAndUnits import *


class SceneObject:
    name = ""

    def __init__(self, name):
        self.name = name

    def hasInside(self, sp):
        return False  # to be overridden (when relevant)

    def hasInside(self, p):
        return self.hasInside(p.position)


allSceneObjects = []


def indexOf(so):
    if so in allSceneObjects:
        return allSceneObjects.index(so)
    return -1


def addSceneObject(so):
    allSceneObjects.append(so)


maxTurn = 35  # degrees self version: the same for all robots
maxSpeed = 1  # m/sec self version: the same for all robots


class Robot(SceneObject):
    pose = Pose()
    diameter = 0.3  # meters

    def __init__(self, *args, **kwargs):
        SceneObject.__init__(self, kwargs.get("n"))
        self.name = kwargs.get("n")
        if "po" in kwargs:
            self.pose = kwargs.get("po")
        elif "ps" and "d" in kwargs:
            self.pose = Pose(pp=kwargs.get("ps"), dd=kwargs.get("d"))
        addSceneObject(self)

    def set(self, p, d):
        self.pose = Pose(ss=p, dd=d)

    def set(self, p):
        self.pose = p

    def hasInside(self, sp):
        x = self.pose.position.x
        y = self.pose.position.y
        return x - self.diameter / 2 <= sp.x <= x + self.diameter / 2 and y - self.diameter / 2 <= sp.y <= y + self.diameter / 2

    def overlappingOther(self):
        x = self.pose.position.x
        y = self.pose.position.y
        r = self.diameter / 2
        result = False
        for i in allSceneObjects:
            if self not in allSceneObjects:
                if allSceneObjects.hasInside(p(x + r, y + r)):
                    result = True
                if allSceneObjects[i].hasInside(p(x - r, y + r)):
                    result = True
                if allSceneObjects[i].hasInside(p(x + r, y - r)):
                    result = True
                if allSceneObjects[i].hasInside(p(x - r, y - r)): result = True
        return result

    def runaway(self):
        x = self.pose.position.x
        y = self.pose.position.y
        r = self.diameter / 2
        result = False
        if p(x + r, y + r).runaway():
            result = True
        if p(x - r, y + r).runaway():
            result = True
        if p(x + r, y - r).runaway():
            result = True
        if p(x - r, y - r).runaway():
            result = True
        return result


# easy constructors
def robot(n):
    return Robot(n)


def robot(n, p):
    Robot(n, po=p)


def robot(n, p, d):
    return Robot(n, ps=p, d=d)


class RestrictedArea(SceneObject):
    lowerLeft = ScenePoint
    upperRight = ScenePoint

    def __init__(self, *args, ** kwargs):
        SceneObject.__init__(self, kwargs.get("n"))
        # adjust so two corner points really becomes lowerLeft,upperRight
        x0 = min(kwargs.get("ll").x, kwargs.get("ur").x)
        x1 = max(kwargs.get("ll").x, kwargs.get("ur").x)
        y0 = min(kwargs.get("ll").y, kwargs.get("ur").y)
        y1 = max(kwargs.get("ll").y, kwargs.get("ur").y)
        ll = ScenePoint(x0, y0)
        ur = ScenePoint(x1, y1)
        self.name = kwargs.get("n")
        self.lowerLeft = ll
        if "ur" in kwargs:
            self.upperRight = ur
        elif "width" and "depth" in kwargs:
            self.upperRight = ScenePoint(ll.x + kwargs.get("width"), ll.y + kwargs.get("depth"))
        addSceneObject(self)

    def hasInside(self, p):
        return self.lowerLeft.x <= p.x <= self.upperRight.x and self.lowerLeft.y <= p.y <= self.upperRight.y


# easy constructors
def restrictedArea(n, corner1, corner2):
    return RestrictedArea(n, corner1, corner2)


def restrictedArea(n, ll, width, depth):
    return RestrictedArea(n, ll, width, depth)


class ReferencePoint(SceneObject):
    point = ScenePoint

    def __init__(self, p, *args, **kwargs):
        if "n" in kwargs:
            SceneObject.__init__(self, kwargs.get("n"))
            self.name = kwargs.get("n")
        else:
            SceneObject.__init__(self, "")
            self.name = ""
        self.point = p.klone()
        addSceneObject(self)

# easy constructors
def referencePoint(p):
    return ReferencePoint(p)


def referencePoint(n, p):
    return ReferencePoint(p, n=n)


def referencePoint(x, y):
    return ReferencePoint(ScenePoint(x, y))


def referencePoint(n, x, y):
    return ReferencePoint(ScenePoint(x, y), n=n)


class Grid(SceneObject):
    resolution = 0

    def __init__(self, *args, **kwargs):
        SceneObject.__init__(self, "Grid")
        self.name = "Grid"
        if "r" in kwargs:
            self.resolution = kwargs.get("r")
        else:
            self.resolution = 1
        addSceneObject(self)


# easy constructors
def grid(r):
    return Grid(r=r)


def grid():
    return Grid()

if __name__ == "__main__":
    print("Testing Robot constructors: ")
    Robot()
    robot()

