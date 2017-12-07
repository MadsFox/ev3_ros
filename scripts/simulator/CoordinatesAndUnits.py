#!/usr/bin/env python
from simulator import *
from math import *

# scene coordinate system
#    x-axis front edge of scene shown in bottom of screen window
#     and with zero in the middle
#    y-axis points into the scene zero at front edge of scene
# internal units are meters

m = 1
sw = sceneWidth
hsw = sceneWidth / 2
sd = sceneDepth


def toScreenUnit(sceneDist):
    return sceneDist / sceneWidth * width


class ScreenPoint:
    x = 0
    y = 0

    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy


class ScenePoint:
    x = 0
    y = 0

    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy

    def klone(self):
        return self.ScenePoint(self.x, self.y)

    def toScreenPoint(self):
        scrX = round(width / 2 + self.x / sceneWidth * width)
        scrY = round(height - self.y / sceneDepth * height)
        return ScreenPoint(scrX, scrY)

    def toString(self):
        return "<" + self.x + "," + self.y + ">"

    def runaway(self):
        return self.x > hsw or self.x < -hsw or self.y > sd or self.y < 0

    def moveRelXRelY(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY

    def moveRelPhiD(self, phi, deltaDist):
        sinNewDir = sin(radians(phi))
        cosNewDir = cos(radians(phi))
        self.moveRelXRelY(sinNewDir * deltaDist, cosNewDir * deltaDist)


# easy constructor
def p(x, y):
    return ScenePoint(x, y)


def dist(p1, p2):
    return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))


def avg(p1, p2):
    return ScenePoint((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


class Pose:  # for a robot
    position = ScenePoint
    direction = 0  # 0..360

    def __init__(self, *args, **kwargs):
        if "xx" and "yy" in kwargs:
            self.position = ScenePoint(kwargs.get("x"), kwargs.get("y"))
        elif "ss" in kwargs:
            self.position = kwargs.get("ss")
        self.direction = kwargs.get("dd")

    def klone(self):
        return Pose(self.position.klone(),
                    self.direction)  # intuitively same as clone, but returns object of right class

    def toString(self):
        return self.position + "*phi=" + self.direction

    def moveRelPhiD(self, deltaPhi, deltaDist):
        # phi added to current direction, but scaled by deltaDist AND SOME CONSTANT THAT DEPENDS ON PHYSICAL DETAILS OF THE ROBOT
        self.moveAbsPhiD(self.direction + deltaPhi * abs(deltaDist) * 4, deltaDist)

    def moveAbsPhiD(self, phi, deltaDist):
        # set direction and move
        self.direction = normalizeAngle(phi)
        self.position.moveRelPhiD(self.direction, deltaDist)


# easy constructor:
def pose(x, y, d):
    return Pose(xx=x, yy=y, dd=d)


def pose(s, d):
    return Pose(ss=s, dd=d)


def avg(p1, p2):
    return Pose(ss=avg(p1.position, p2.position), dd=(p1.direction + p2.direction) / 2)


# directions internally in degrees memotech. as n,e,s,w etc.
# south means looking out of from scene towards audience

north = 0
east = 90
south = 180
west = 270
northEast = north + 90 / 2
southEast = south - 90 / 2
northWest = west + 90 / 2
southWest = west - 90 / 2
nne = north + 90 / 4
ene = east - 90 / 4
ese = east + 90 / 4
sse = south - 90 / 4
ssw = south + 90 / 4
wsw = west - 90 / 4
wnw = west + 90 / 4
nnw = 360 - 90 / 4


def normalizeAngle(phi):
    if phi < 0:
        return normalizeAngle(phi + 360)
    elif phi >= 360:
        return normalizeAngle(phi - 360)
    else:
        return phi


def normalizeAngleRad(phi):
    if phi < 0:
        return normalizeAngle(phi + 2 * pi)
    elif phi >= 2 * pi:
        return normalizeAngle(phi - 2 * pi)
    else:
        return phi


robotTurningDiameter = 0.7


# Currently only used for checking feasibility of generated route
# in mkXXXXXRouteXXXX should be correlated with constant epsilon and expected robot diameter

def dist(p1, p2):
    # plain euclidian, ignoring direction
    return dist(p1.position, p2.position)


def dist(p1, p2): return dist(p1.position, p2)


def dist(p1, p2): return dist(p1, p2.position)
