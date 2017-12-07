#!/usr/bin/env python

from manuscript import *

sceneWidth = 10  # meters
sceneDepth = 5  # meters
width = 2000
height = 1000

scriptFileName = "hubahop"

if __name__ == "__main__":
    # the following should preserve the proportions of (sceneWidth,sceneDepth)
    manuscript()
    sortEventList()  # IMPORTANT!!!!
    # printEventList()
    initTime()
