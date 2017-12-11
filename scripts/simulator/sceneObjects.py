#!/usr/bin/env python

from CoordinatesAndUnits import *


class SceneObject:
    name = ""

    def __init__(self, name):
        self.name = name

    def has_inside(self, po):
        if isinstance(po, ScenePoint):
            return False
        elif isinstance(po, Pose):
            return self.has_inside(po.position)


allSceneObjects = []


def index_of(so):
    if so in allSceneObjects:
        return allSceneObjects.index(so)
    return -1


def add_scene_object(so):
    allSceneObjects.append(so)


maxTurn = 35  # degrees self version: the same for all robots
maxSpeed = 1  # m/sec self version: the same for all robots


class Robot(SceneObject):
    pose = None
    diameter = 0.3  # meters

    def __init__(self, n, po=None, d=None):
        SceneObject.__init__(self, n)
        self.name = n
        if d is None:
            self.pose = po
        elif d and po is not None:
            self.pose = Pose(po, d)
        add_scene_object(self)

    def set(self, po, d=None):
        if d is None:
            self.pose = po
        else:
            self.pose = Pose(po, d)

    def has_inside(self, sp):
        x = self.pose.position.x
        y = self.pose.position.y
        return (x - self.diameter / 2 <= sp.x <= x + self.diameter / 2 and
                y - self.diameter / 2 <= sp.y <= y + self.diameter / 2)

    def overlapping_other(self):
        x = self.pose.position.x
        y = self.pose.position.y
        r = self.diameter / 2
        result = False
        for i in allSceneObjects:
            if self is not i:
                if allSceneObjects[i].has_inside(p(x + r, y + r)):
                    result = True
                if allSceneObjects[i].has_inside(p(x - r, y + r)):
                    result = True
                if allSceneObjects[i].has_inside(p(x + r, y - r)):
                    result = True
                if allSceneObjects[i].has_inside(p(x - r, y - r)):
                    result = True
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
def robot(n, po=None, d=None):
    if d is None:
        return Robot(n, po)
    elif po and d is None:
        return Robot(n)
    else:
        return Robot(n, po, d)


class RestrictedArea(SceneObject):
    lowerLeft = ScenePoint
    upperRight = ScenePoint

    def __init__(self, n, ll, w, d=None):
        SceneObject.__init__(self, n)
        # adjust so two corner points really becomes lowerLeft,upperRight
        self.name = n
        if d is None:
            x0 = min(ll.x, w.x)
            x1 = max(ll.x, w.x)
            y0 = min(ll.y, w.y)
            y1 = max(ll.y, w.y)
            self.lowerLeft = ScenePoint(x0, y0)
            self.upperRight = ScenePoint(x1, y1)
        else:
            self.lowerLeft = ll
            self.upperRight = ScenePoint(ll.x+w, ll.y+d)
        add_scene_object(self)

    def has_inside(self, po):
        return self.lowerLeft.x <= po.x <= self.upperRight.x and self.lowerLeft.y <= po.y <= self.upperRight.y


# easy constructors
def restricted_area(n, ll, w, d=None):
    if d is None:
        return RestrictedArea(n, ll, w)
    else:
        return RestrictedArea(n, ll, w, d)


class ReferencePoint(SceneObject):
    point = ScenePoint

    def __init__(self, n, po=None):
        if p is None:
            SceneObject.__init__(self, "")
            self.name = ""
            self.point = po.klone()
        else:
            SceneObject.__init__(self, n)
            self.name = n
            self.point = po
        add_scene_object(self)


# easy constructors
def reference_point(n, x=None, y=None):
    if x and y is None:
        return ReferencePoint(n)
    elif y is None and isinstance(x, ScenePoint):
        return ReferencePoint(n, x)
    elif y is None and isinstance(x, int):
        return ReferencePoint(ScenePoint(n, x))
    else:
        return ReferencePoint(n, ScenePoint(x, y))


class Grid(SceneObject):
    resolution = 0

    def __init__(self, r=None):
        SceneObject.__init__(self, "Grid")
        self.name = "Grid"
        if r is None:
            self.resolution = 1
        else:
            self.resolution = r
        add_scene_object(self)


# easy constructors
def grid(r=None):
    if r is None:
        return Grid()
    else:
        return Grid(r)


if __name__ == "__main__":
    print("Testing Robot constructors: ")
    print('Robot("palle"): {}'.format(Robot("palle")))
    print('Robot("palle", ScenePoint(10, 20), 90): {}'.format(Robot("palle", ScenePoint(10, 20), 90)))
    print('Robot("palle", Pose(10, 20, 90): {}'.format(Robot("palle", ScenePoint(10, 20), 90)))
    print('robot("palle"): {}'.format(robot("palle")))
    print('robot("palle", ScenePoint(10, 20), 90): {}'.format(robot("palle", ScenePoint(10, 20), 90)))
    print('robot("palle", Pose(10, 20, 90): {}'.format(robot("palle", ScenePoint(10, 20), 90)))
