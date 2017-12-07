#!/usr/bin/env python

from CoordinatesAndUnits import *

sceneWidth = 10 #meters
sceneDepth = 5 #meters

scriptFileName = "hubahop"

if __name__ == "__main__":
  # the following should preserve the proportions of (sceneWidth,sceneDepth)
  manuscript()
  sortEventList() # IMPORTANT!!!!
  #printEventList()
  initTime()