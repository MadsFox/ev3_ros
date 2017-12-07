class SceneObject {
  String name;
  color col;
  void draw() {;} // to be overridden  
  boolean hasInside(ScenePoint sp) {return false;} // to be overridden (when relevant)
  boolean hasInside(Pose p) {return hasInside(p.position);}
}

SceneObject [] allSceneObjects = new SceneObject[0];

void drawAllSceneObjects() {
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof RestrictedArea)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof Grid)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof ReferencePoint)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof Robot)allSceneObjects[i].draw();}

int indexOf(SceneObject so) {
  for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i]==so)return i;
  return -1;
}

void addSceneObject(SceneObject so) {
  SceneObject [] old = allSceneObjects;
  allSceneObjects = new SceneObject[old.length+1];
  for(int i=0;i<old.length;i++)allSceneObjects[i]=old[i];
  allSceneObjects[old.length]=so;
}


float maxTurn=35; // degrees; this version: the same for all robots
float maxSpeed= 1; // m/sec; this version: the same for all robots

class Robot extends SceneObject{
  Pose pose;
  float diameter = 0.3; //meters

  Robot(String n, color c) {name=n;col=c;addSceneObject(this);}
  
  Robot(String n, color c, Pose p) {name=n;col=c;pose=p;addSceneObject(this);}
  
  Robot(String n, color c, ScenePoint p, float d) {name=n;col=c;pose=new Pose(p,d);addSceneObject(this);}

  void set(ScenePoint p, float d) {pose=new Pose(p,d);}

  void set(Pose p) {pose=p;}

  @ Override
  void draw() {
    ScreenPoint p=pose.position.toScreenPoint();
    float sr=toScreenUnit(diameter/2);
    stroke(0);
    strokeWeight(2);
    fill(col);
    ellipse(p.x, p.y,
            2*sr, 2*sr);
    float sinDir=sin(radians(pose.direction)); float cosDir=cos(radians(pose.direction));
    line(p.x+sr*sinDir,p.y-sr*cosDir, p.x-sr*sinDir,p.y+sr*cosDir);
    //stroke(255,0,0);
    line( p.x+sr*sinDir,p.y-sr*cosDir, p.x-sr*cosDir,p.y-sr*sinDir);
    line( p.x+sr*sinDir,p.y-sr*cosDir,  p.x+sr*cosDir,p.y+sr*sinDir);
    
    if(overlappingOther()) drawWarningFrame();
    if(runaway()) {drawWarningFrame();drawWarningOnEdges();}
    
    
  }
  
//  void moveTo(Pose p) {pose=p;}

  @ Override
  boolean hasInside(ScenePoint sp) {
    float x=pose.position.x; float y=pose.position.y;
    return x-diameter/2<=sp.x && sp.x<=x+diameter/2 && y-diameter/2<=sp.y && sp.y<=y+diameter/2;
  }
    
  boolean overlappingOther() {
    float x=pose.position.x; float y=pose.position.y;
    float r=diameter/2;
    boolean result=false;
    for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i]!=this) {
      if( allSceneObjects[i].hasInside(p(x+r,y+r)) ) result=true;
      if( allSceneObjects[i].hasInside(p(x-r,y+r)) ) result=true;
      if( allSceneObjects[i].hasInside(p(x+r,y-r)) ) result=true;
      if( allSceneObjects[i].hasInside(p(x-r,y-r)) ) result=true;
    }
    return result;
  }
  
  boolean runaway() {
    float x=pose.position.x; float y=pose.position.y;
    float r=diameter/2;
    boolean result = false;
    if(p(x+r,y+r).runaway()) result=true;
    if(p(x-r,y+r).runaway()) result=true;
    if(p(x+r,y-r).runaway()) result=true;
    if(p(x-r,y-r).runaway()) result=true;
    return result;
  }
  
  void drawWarningFrame() {
    ScreenPoint c=pose.position.toScreenPoint();
    float sr=toScreenUnit(diameter/2);
    float x1=c.x-sr-3; float x2=c.x+sr+3;
    float y1=c.y-sr-3; float y2=c.y+sr+3;
    stroke(color(255,0,0)); strokeWeight(3);
    line(x1,y1,x1,y2);
    line(x1,y1,x2,y1);
    line(x2,y2,x1,y2);
    line(x2,y2,x2,y1);
  }

  void drawWarningOnEdges() {
    // only relevants for runaway robots
    ScreenPoint c=pose.position.toScreenPoint();
    float sr=toScreenUnit(diameter/2);
    float x1=c.x-sr-3; float x2=c.x+sr+3;
    float y1=c.y-sr-3; float y2=c.y+sr+3;
    stroke(color(255,0,0)); strokeWeight(3);
    if(x1>width && y2<height && y2>0) {line(width-2,y1,width-2,y2);}
    if(x1<0 && y2<height && y2>0) {line(2,y1,2,y2); return;}
    if(y1>height && x2<width && x2>0) {line(x1,height-2,x2,height-2);}
    if(y1<0 && x2<width && x2>0) {line(x1,2,x2,2);}
    fill(color(255,0,0));
    if(x1<0 && y2>height) {rect(1,height-5-1,5,5);}
    if(x2>width && y2>height) {rect(width-5-1,height-5-1,5,5);}
    if(x1<0 && y1<0) {rect(1,1,5,5);}
    if(x2>width && y1<0) {rect(width-5-1,1,5,5);}
  }
}
// easy constructors
Robot robot(String n, color c) {return new Robot(n, c);}
Robot robot(String n, color c, Pose p) {return new Robot(n, c, p);}
Robot robot(String n, color c, ScenePoint p, float d) {return new Robot(n, c, p, d);}




class RestrictedArea extends SceneObject{
  ScenePoint lowerLeft;
  ScenePoint upperRight;
  
  RestrictedArea(String n, color c,ScenePoint ll, ScenePoint ur) {
       // adjust so two corner points really becomes lowerLeft,upperRight
       float x0=min(ll.x,ur.x); float x1=max(ll.x,ur.x); 
       float y0=min(ll.y,ur.y); float y1=max(ll.y,ur.y);
       ll=new ScenePoint(x0,y0); ur=new ScenePoint(x1,y1);
       name=n;col=c;lowerLeft=ll;upperRight=ur;addSceneObject(this);}
  RestrictedArea(String n, color c,ScenePoint ll, float width, float depth) {name=n;col=c;
    lowerLeft=ll;upperRight=new ScenePoint(ll.x+width,ll.y+depth);addSceneObject(this);}
  
  
  @ Override
  boolean hasInside(ScenePoint p) {return lowerLeft.x<=p.x && p.x<=upperRight.x && lowerLeft.y<=p.y && p.y<=upperRight.y;}
  
  @ Override
  void draw() {
    fill(col);
    stroke(col);
    ScreenPoint llsp=lowerLeft.toScreenPoint(); ScreenPoint ursp=upperRight.toScreenPoint();
    rect(llsp.x,ursp.y,ursp.x-llsp.x,llsp.y-ursp.y);
  }
}
// easy constructors
RestrictedArea restrictedArea(String n, color c,ScenePoint corner1, ScenePoint corner2)
  {return new RestrictedArea(n, c,corner1, corner2);}
RestrictedArea restrictedArea(String n, color c,ScenePoint ll, float width, float depth)
  {return new RestrictedArea(n, c,ll, width, depth);}

class ReferencePoint extends SceneObject{
  ScenePoint point;
  
  ReferencePoint(ScenePoint p){point=p.klone();addSceneObject(this);name="";col=color(255,255,255);}
  ReferencePoint(color c, ScenePoint p){point=p.klone();addSceneObject(this);name="";col=c;}
  ReferencePoint(String n, color c, ScenePoint p){point=p.klone();addSceneObject(this);name=n;col=c;}

  @ Override
  void draw(){stroke(col);strokeWeight(5);
    ScreenPoint p = point.toScreenPoint();
    line(p.x-10,p.y,p.x+10,p.y);
    line(p.x,p.y-10,p.x,p.y+10);
  }
}

// easy constructors
ReferencePoint referencePoint(ScenePoint p) {return new ReferencePoint(p);}
ReferencePoint referencePoint(color c, ScenePoint p) {return new ReferencePoint(c,p);}
ReferencePoint referencePoint(String n, color c, ScenePoint p) {return new ReferencePoint(n,c,p);}
ReferencePoint referencePoint(float x, float y) {return new ReferencePoint(new ScenePoint(x,y));}
ReferencePoint referencePoint(color c, float x, float y) {return new ReferencePoint(c,new ScenePoint(x,y));}
ReferencePoint referencePoint(String n, color c, float x, float y) {return new ReferencePoint(n,c,new ScenePoint(x,y));}


class Grid extends SceneObject{
  float resolution;
  Grid(color c, float r) {name="Grid";col=c;resolution=r;addSceneObject(this);}
  Grid(float r) {name="Grid";col=color(255,255,255);resolution=r;addSceneObject(this);}
  Grid(color c) {name="Grid";col=c;resolution=1;addSceneObject(this);}
  Grid() {name="Grid";col=color(255,255,255);resolution=1;addSceneObject(this);}

  @ Override
  void draw(){stroke(col);strokeWeight(2);
    line(width/2,0,width/2,height);
    line(0,height/2,width,height/2);
    strokeWeight(1);
    float r=toScreenUnit(resolution);
    float d=r;
    while(d<=height/2) {line(0,height/2+d,width,height/2+d);line(0,height/2-d,width,height/2-d);d+=r;}
    d=r;
    while(d<=width/2) {line(width/2+d,0,width/2+d,height);line(width/2-d,0,width/2-d,height);d+=r;}
  }
}
// easy constructors
Grid grid(color c, float r) {return new Grid(c,r);}
Grid grid(float r) {return new Grid(r);}
Grid grid(color c) {return new Grid();}
Grid grid() {return new Grid();}