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


def set_scene_width(w):
    global sw
    sw = w
    global hsw
    hsw = sw/2


def set_scene_depth(h):
    global sd
    sd = h


def set_width(w):
    global width
    width = w


def set_height(h):
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

    def to_string(self):
        return "<{},{}>".format(self.x, self.y)

    def runaway(self):
        return self.x > hsw or self.x < -hsw or self.y > sd or self.y < 0

    def move_rel_x_rel_y(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    def move_rel_phi_d(self, phi, delta_dist):
        sin_new_dir = sin(radians(phi))
        cos_new_dir = cos(radians(phi))
        self.move_rel_x_rel_y(sin_new_dir * delta_dist, cos_new_dir * delta_dist)

    def avg(self, point):
        return ScenePoint((self.x + point.x) / 2, (self.y + point.y) / 2)


# easy constructor
def sp(x, y):
    return ScenePoint(x, y)


class Pose(ScenePoint):  # for a robot
    direction = 0  # 0..360

    def __init__(self, xx, yy, *args):
        if len(args) < 1:
            ScenePoint.__init__(self, xx.x, xx.y)
            self.direction = yy
        else:
            ScenePoint.__init__(self, xx, yy)
            self.direction = args[0]

    def klone(self):
        return Pose(self.x, self.y, self.direction)  # intuitively same as clone, but returns object of right class

    def to_string(self):
        return "<{},{}*phi={}>".format(self.x, self.y, self.direction)

    def runaway(self):
        return self.runaway()

    def move_rel_phi_d(self, delta_phi, delta_dist):
        # phi added to current direction, but scaled by deltaDist
        # AND SOME CONSTANT THAT DEPENDS ON PHYSICAL DETAILS OF THE ROBOT
        self.move_abs_phi_d(self.direction + delta_phi * abs(delta_dist) * 4, delta_dist)

    def move_abs_phi_d(self, phi, delta_dist):
        # set direction and move
        self.direction = normalize_angle(phi)
        self.move_rel_phi_d(self.direction, delta_dist)

    def avg(self, po):
        return Pose((self.x + po.x) / 2, (self.y + po.y) / 2, (self.direction + po.direction) / 2)


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


def normalize_angle(phi):
    if phi < 0:
        return normalize_angle(phi + 360)
    elif phi >= 360:
        return normalize_angle(phi - 360)
    else:
        return phi


def normalize_angle_rad(phi):
    if phi < 0:
        return normalize_angle(phi + 2 * pi)
    elif phi >= 2 * pi:
        return normalize_angle(phi - 2 * pi)
    else:
        return phi


robotTurningDiameter = 0.7


# Currently only used for checking feasibility of generated route
# in mkXXXXXRouteXXXX should be correlated with constant epsilon and expected robot diameter

def dist(p1, p2):
    return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))


if __name__ == '__main__':
    set_height(2000)
    set_width(1000)
    set_scene_depth(50)
    set_scene_width(100)
    print("testing setHeight(2000): {}".format(height))
    print("setWidth(1000):          {}".format(width))
    print("setSceneDepth(5):        {}".format(sd))
    print("setSceneWidth(100):      {}".format(sw))
    print("half SceneWidth:         {}".format(hsw))

    print("")
    print("Testing ScenePoint")

    s = ScenePoint(10, 20)
    s2 = s.klone()
    s3 = sp(10, 30)
    print("s = ScenePoint(10, 20):  {}".format(s.to_string()))
    print("s2 = s.clone():          {}".format(s2.to_string()))
    print("s3 = p(20, 30):          {}".format(s3.to_string()))

    print("s.runaway():             {}".format(s.runaway()))

    s.move_rel_phi_d(90, sw)
    print("s.moveRelPhiD(90, sw):   {}".format(s.to_string()))

    print("s.runaway():             {}".format(s.runaway()))

    s.move_rel_phi_d(90, -sw)
    print("s.moveRelPhiD(90, -sw):  {}".format(s.to_string()))

    s.move_rel_x_rel_y(sw, 0)
    print("s.moveRelXRelY(sw, 0):   {}".format(s.to_string()))
    s.move_rel_x_rel_y(-sw, 0)
    print("s.moveRelXRelY(-sw, 0):  {}".format(s.to_string()))

    print("dist(s, s3):             {}".format(dist(s, s3)))

    print("s.avg(s3):               {}".format(s.avg(s3).to_string()))

    print("")
    print("Testing ScenePoint")

    p = Pose(10, 20, 90)
    pk = s.klone()
    p3 = pose(10, 30, 0)
    print("p = Pose(10, 20):        {}".format(p.to_string()))
    print("pk = s.clone():          {}".format(pk.to_string()))
    print("p3 = pose(20, 30, 0):    {}".format(p3.to_string()))

    print("p.runaway():             {}".format(p.runaway()))

    p.move_rel_phi_d(0, sw)
    print("p.moveRelPhiD(90, sw):   {}".format(p.to_string()))

    print("p.runaway():             {}".format(p.runaway()))

    p.move_rel_phi_d(90, -sw)
    print("p.moveRelPhiD(90, -sw):  {}".format(p.to_string()))

    p.move_abs_phi_d(90, 0)
    print("p.moveRelXRelY(sw, 0):   {}".format(p.to_string()))
    p.move_abs_phi_d(-90, 0)
    print("p.moveRelXRelY(-sw, 0):  {}".format(p.to_string()))

    print("dist(p, p3):             {}".format(dist(p, p3)))

    print("p.avg(p3):               {}".format(p.avg(p3).to_string()))
