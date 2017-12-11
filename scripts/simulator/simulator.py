#!/usr/bin/env python

from manuscript import *

sceneWidth = 10  # meters
sceneDepth = 5  # meters
width = 2000
height = 1000

scriptFileName = "hubahop"

if __name__ == "__main__":
    set_scene_width(sceneWidth)
    set_scene_depth(sceneDepth)
    set_width(width)
    set_height(height)
    # the following should preserve the proportions of (sceneWidth,sceneDepth)
    manuscript()
    sort_event_list()  # IMPORTANT!!!!
    # printEventList()
    init_time()
