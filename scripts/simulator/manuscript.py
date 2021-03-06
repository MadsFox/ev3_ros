#!/usr/bin/env python
from manuscriptHelpers import *


# the method manuscript initiates some data structures, but does not make anything happen

def manuscript():
    grid()
    referencePoint(hsw / 2, sd / 2)
    referencePoint(-hsw / 2, sd / 2)

    restrictedArea("green stuff", p(-hsw + 0.5, sd - 1.75), p(-hsw + 3, sd - 2))
    restrictedArea("light stuff", p(0.5, 0.5), p(hsw - 2, 1))

    nille = robot("Nille")
    frederik = robot("Frederik")

    initialPose(nille, pose(hsw / 2 + 1, sd / 4, west))  # initialPose skal komme før wait, follow..., osv.
    initialPose(frederik, pose(hsw / 2, sd / 4 + 1, south))
    # meetAndGreat(nille, frederik, -hsw/2, sd/2)
    wait(nille, 2)

    moveTo(nille, pose(-hsw / 2, sd / 2, south))
    moveTo(frederik, pose(hsw / 2, sd / 4, south))

    moveTo(nille, pose(-hsw / 4, sd * 0.75, north))
    moveTo(frederik, pose(-hsw / 2, sd / 2, south))
    moveTo(frederik, pose(-hsw / 4 - 0.5, sd / 2 - 0.5, east))

    moveTo(nille, pose(-hsw / 8, sd / 4, south))
    moveTo(frederik, pose(+hsw / 8, sd / 4, south))

    wait(nille, 3)

    synchronize()  # denne her er fiks: alle venter til sidste mand følger trop

    moveToBacking(nille, pose(-hsw / 8 + 1, sd / 4 + 1, south))
    moveToBacking(frederik, pose(+hsw / 8 + 1, sd / 4 + 1, south))

    wait(nille, 0.5)
    wait(frederik, 0.5)

    moveTo(nille, pose(+hsw / 8 + 1.5, sd / 4, south))
    moveTo(frederik, pose(+hsw / 8 + 2, sd / 4, south))

    synchronize()
    moveTo(nille, pose(-1, sd / 2, east))
    moveToBacking(frederik, pose(1, sd / 2, west))

    synchronize()

    moveTo(nille, pose(-0.25, sd / 2, east))
    moveTo(frederik, pose(0.25, sd / 2, west))

    moveToBacking(nille, pose(-1, sd / 2 - 0.75, nne))
    moveTo(nille, pose(-1, sd / 2, north))

    moveToBacking(frederik, pose(1, sd / 2 + 0.75, ssw))
    moveTo(frederik, pose(1, sd / 2, south))

    circleRight(nille, 0.75, 180)
    circleRight(frederik, 0.75, 180)
    circleRight(nille, 0.375, 180)
    circleRight(frederik, 0.375, 180)
    circleRightBacking(nille, 0.375, 40)
    circleRight(frederik, 0.375, 40)
    circleRight(nille, 0.375, 40)
    circleRightBacking(frederik, 0.375, 40)

    moveToBacking(nille, pose(0, sd / 2 - 0.75, north))
    moveToBacking(frederik, pose(0, sd / 2 + 0.75, south))

    moveTo(nille, pose(0, sd / 2 - 0.1, north))  # north
    moveTo(frederik, pose(0, sd / 2 + 0.1, south))
    moveToBacking(nille, pose(-0.5, sd / 2 - 0.75, nne))
    moveToBacking(frederik, pose(0.5, sd / 2 + 0.75, ssw))

    moveTo(nille, pose(1, sd + 2, north))
    circleRight(frederik, 0.5, 180)
    wait(frederik, 0.5)
    moveTo(frederik, pose(1, sd + 2, north))


def meetAndGreat(r1, r2, x, y):
    moveTo(r1, x - 1, y, east)
    moveTo(r2, x + 1, y, west)
    synchronize(r1, r2)
    moveTo(r1, x - 0.25, y, east)
    moveTo(r2, x + 0.25, y, west)
    wait(r1, 1)
    wait(r2, 1)
    moveToBacking(r1, x - 1, y, east)
    moveToBacking(r2, x + 1, y, west)
    wait(r1, 0.5)
    wait(r2, 0.5)
