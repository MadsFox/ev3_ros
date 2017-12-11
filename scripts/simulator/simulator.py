#!/usr/bin/env python

from manuscript import *

sceneWidth = 10  # meters
sceneDepth = 5  # meters
width = 2000
height = 1000

scriptFileName = "hubahop"

if __name__ == "__main__":
    setSceneWidth(sceneWidth)
    setSceneDepth(sceneDepth)
    setWidth(width)
    setHeight(height)
    # the following should preserve the proportions of (sceneWidth,sceneDepth)
    manuscript()
    sortEventList()  # IMPORTANT!!!!
    # printEventList()
    initTime()
