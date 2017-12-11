#!/usr/bin/env python
from math import *

# scene coordinate system
#    x-axis front edge of scene shown in bottom of screen window
#     and with zero in the middle
#    y-axis points into the scene zero at front edge of scene
# internal units are meters

m = 1
sw = None
hsw = None
sd = None
width = None
height = None

def setSceneWidth(width):
    global sw
    sw = width
    global hsw
    hsw = sw/2


def setSceneDepth(height):
    global sd
    sd = height


def setWidth(w):
    global width
    width = w


def setHeight(h):
    global height
    height = h


class ScenePoint:
    x = 0
    y = 0

    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy

    def klone(self):
        return ScenePoint(self.x, self.y)

    def toString(self):
        return "<{},{}>".format(self.x, self.y)

    def runaway(self):
        return self.x > hsw or self.x < -hsw or self.y > sd or self.y < 0

    def moveRelXRelY(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY

    def moveRelPhiD(self, phi, deltaDist):
        sinNewDir = sin(radians(phi))
        cosNewDir = cos(radians(phi))
        self.moveRelXRelY(sinNewDir * deltaDist, cosNewDir * deltaDist)

    def avg(self, point):
        return ScenePoint((self.x + point.x) / 2, (self.y + point.y) / 2)


# easy constructor
def p(x, y):
    return ScenePoint(x, y)


class Pose:  # for a robot
    position = ScenePoint
    direction = 0  # 0..360

    def __init__(self, xx, yy, dd=None):
        if dd is None:
            self.position = xx
            self.direction = yy
        else:
            self.position = ScenePoint(xx, yy)
            self.direction = dd

    def klone(self):
        return Pose(self.position.klone(),
                    self.direction)  # intuitively same as clone, but returns object of right class

    def toString(self):
        return "<{},{}*phi={}>".format(self.position.x, self.position.y, self.direction)

    def runaway(self):
        return self.position.runaway()

    def moveRelPhiD(self, deltaPhi, deltaDist):
        # phi added to current direction, but scaled by deltaDist AND SOME CONSTANT THAT DEPENDS ON PHYSICAL DETAILS OF THE ROBOT
        self.moveAbsPhiD(self.direction + deltaPhi * abs(deltaDist) * 4, deltaDist)

    def moveAbsPhiD(self, phi, deltaDist):
        # set direction and move
        self.direction = normalizeAngle(phi)
        self.position.moveRelPhiD(self.direction, deltaDist)

    def avg(self, pose):
        return Pose(self.position.avg(pose.position), (self.direction + pose.direction) / 2)


# easy constructor:
def pose(x, y, d=None):
    if d is None:
        return Pose(x, y)
    else:
        return Pose(x, y, d)


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
    if isinstance(p1, Pose) and isinstance(p2, Pose):
        p1 = p1.position
        p2 = p2.position
    elif isinstance(p1, ScenePoint) and isinstance(p2, Pose):
        p2 = p2.position
    elif isinstance(p1, Pose) and isinstance(p2, ScenePoint):
        p1 = p1.position
    return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))


if __name__ == '__main__':
    setHeight(2000)
    setWidth(1000)
    setSceneDepth(50)
    setSceneWidth(100)
    print("testing setHeight(2000): {}".format(height))
    print("setWidth(1000):          {}".format(width))
    print("setSceneDepth(5):        {}".format(sd))
    print("setSceneWidth(100):      {}".format(sw))
    print("half SceneWidth:         {}".format(hsw))

    print("")
    print("Testing ScenePoint")

    s = ScenePoint(10, 20)
    s2 = s.klone()
    s3 = p(10, 30)
    print("s = ScenePoint(10, 20):  {}".format(s.toString()))
    print("s2 = s.clone():          {}".format(s2.toString()))
    print("s3 = p(20, 30):          {}".format(s3.toString()))

    print("s.runaway():             {}".format(s.runaway()))

    s.moveRelPhiD(90, sw)
    print("s.moveRelPhiD(90, sw):   {}".format(s.toString()))

    print("s.runaway():             {}".format(s.runaway()))

    s.moveRelPhiD(90, -sw)
    print("s.moveRelPhiD(90, -sw):  {}".format(s.toString()))

    s.moveRelXRelY(sw, 0)
    print("s.moveRelXRelY(sw, 0):   {}".format(s.toString()))
    s.moveRelXRelY(-sw, 0)
    print("s.moveRelXRelY(-sw, 0):  {}".format(s.toString()))

    print("dist(s, s3):              {}".format(dist(s, s3)))

    print("s.avg(s3):                {}".format(s.avg(s3).toString()))

    print("")
    print("Testing ScenePoint")

    p = Pose(10, 20, 90)
    pk = s.klone()
    p3 = pose(10, 30, 0)
    print("p = Pose(10, 20):        {}".format(p.toString()))
    print("pk = s.clone():          {}".format(pk.toString()))
    print("p3 = pose(20, 30, 0):    {}".format(p3.toString()))

    print("p.runaway():             {}".format(p.runaway()))

    p.moveRelPhiD(0, sw)
    print("p.moveRelPhiD(90, sw):   {}".format(p.toString()))

    print("p.runaway():             {}".format(p.runaway()))

    p.moveRelPhiD(90, -sw)
    print("p.moveRelPhiD(90, -sw):  {}".format(p.toString()))

    p.moveAbsPhiD(90, 0)
    print("p.moveRelXRelY(sw, 0):   {}".format(p.toString()))
    p.moveAbsPhiD(-90, 0)
    print("p.moveRelXRelY(-sw, 0):  {}".format(p.toString()))

    print("dist(p, p3):              {}".format(dist(p, p3)))

    print("p.avg(p3):                {}".format(p.avg(p3).toString()))


