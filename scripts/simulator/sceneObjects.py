#!/usr/bin/env python

class SceneObject:
  name = ""

  def __init__(self, name):
    self.name = name

  def hasInside(self, sp):
    return False # to be overridden (when relevant)
  
  def hasInside(self, p):
    return self.hasInside(p.position)

allSceneObjects = []

def indexOf(so):
  if so in allSceneObjects:
    return allSceneObjects.index(so)
  return -1

def addSceneObject(so):
  allSceneObjects.append(so)

maxTurn=35 # degrees self version: the same for all robots
maxSpeed= 1 # m/sec self version: the same for all robots

class Robot(SceneObject):
  pose = Pose()
  diameter = 0.3 #meters

  def __init__(self, n):
    SceneObject.__init__(self, n)
    self.name=n
    addSceneObject(self)

  def __init__(self, n, p):
    SceneObject.__init__(self, n)
    self.name = n
    self.pose = p
    addSceneObject(self)

  def __init__(self, n, p, d):
    SceneObject.__init__(self, n)
    self.name = n
    self.pose = Pose(p, d)
    addSceneObject(self)

  def set(self, p, d):
    self.pose= Pose(p,d)

  def set(self, p):
    self.pose=p

  def hasInside(self, sp):
    x = self.pose.position.x
    y = self.pose.position.y
    return x - self.diameter / 2 <= sp.x <= x + self.diameter / 2 and y - self.diameter / 2 <= sp.y and sp.y <= y + self.diameter / 2
    
  def overlappingOther(self):
    x=self.pose.position.x 
    y=self.pose.position.y
    r=self.diameter/2
    result=False
    for i in allSceneObjects: 
      if self not in allSceneObjects:
        if allSceneObjects.hasInside(p(x+r,y+r)):
          result=True
        if allSceneObjects[i].hasInside(p(x-r,y+r)): 
          result=True
        if allSceneObjects[i].hasInside(p(x+r,y-r)): 
          result=True
        if allSceneObjects[i].hasInside(p(x-r,y-r)): result=True
    return result
  
  def runaway(self):
    x=self.pose.position.x 
    y=self.pose.position.y
    r=self.diameter/2
    result = False
    if p(x+r,y+r).runaway(): 
      result=True
    if p(x-r,y+r).runaway(): 
        result=True
    if p(x+r,y-r).runaway(): 
        result=True
    if p(x-r,y-r).runaway(): 
        result=True
    return result
  

# easy constructors
def robot(n):
  return Robot(n)
def robot(n, p):
  Robot(n, p)
def robot(n, p, d):
  return Robot(n, p, d)




class RestrictedArea(SceneObject):
  lowerLeft = ScenePoint
  upperRight = ScenePoint
  
  def RestrictedArea(self,n, ll, ur):
    SceneObject.__init__(self, n)
    self.lowerLeft = ll
    self.upperRight = ur
    # adjust so two corner points really becomes lowerLeft,upperRight
    x0=min(ll.x,ur.x) 
    x1=max(ll.x,ur.x) 
    y0=min(ll.y,ur.y) 
    y1=max(ll.y,ur.y)
    ll=ScenePoint(x0,y0) 
    ur=ScenePoint(x1,y1)
    self.name=n
    self.lowerLeft=ll
    self.upperRight=ur
    addSceneObject(self)
  
  def RestrictedArea(self, n, ll, width, depth):
    SceneObject.__init__(self, n)
    self.name=n
    self.lowerLeft=ll
    self.upperRight=ScenePoint(ll.x+width,ll.y+depth)
    addSceneObject(self)
  
  
  def hasInside(self, p):
    return self.lowerLeft.x <= p.x <= self.upperRight.x and self.lowerLeft.y <= p.y and p.y <= self.upperRight.y
  
# easy constructors
def restrictedArea(n, corner1, corner2):
  return RestrictedArea(n, corner1, corner2)
def restrictedArea(n, ll, width, depth):
  return RestrictedArea(n, ll, width, depth)

class ReferencePoint(SceneObject):
  point = ScenePoint
  
  def ReferencePoint(self, p):
    SceneObject.__init__(self, "")
    self.point=p.klone()
    addSceneObject(self)
    self.name=""

  def ReferencePoint(self, n, p):
    SceneObject.__init__(self, n)
    self.point=p.klone()
    addSceneObject(self)
    self.name=n
      
# easy constructors
def referencePoint(p):
  return ReferencePoint(p)
def referencePoint(c, p):
  return ReferencePoint(c,p)
def referencePoint(n, c, p):
  return ReferencePoint(n,c,p)
def referencePoint(x, y):
  return ReferencePoint(ScenePoint(x,y))
def referencePoint(c, x, y):
  return ReferencePoint(c,ScenePoint(x,y))
def referencePoint(n, c, x, y):
  return ReferencePoint(n,c,ScenePoint(x,y))


class Grid(SceneObject):
  resolution = 0
  def Grid(self, r):
    SceneObject.__init__(self, "Grid")
    self.name="Grid"
    self.resolution=r
    addSceneObject(self)

  def Grid(self):
    SceneObject.__init__(self, "Grid")
    self.name="Grid"
    self.resolution=1
    addSceneObject(self)

# easy constructors
def grid(r):
  return Grid(r)
def grid():
  return Grid()