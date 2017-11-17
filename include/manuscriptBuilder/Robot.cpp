#include "SceneObject.cpp"
#include "Pose.cpp"
#include "ScreenPoint.cpp"

class Robot : public SceneObject{
  public:
    Pose pose;
    float diameter = 0.3; //meters
  
    float maxTurn=35; // degrees; this version: the same for all robots
    float maxSpeed= 1; // m/sec; this version: the same for all robots
  
    Robot(String n) {name=n;addSceneObject(this);}
    
    Robot(String n, Pose p) {name=n;pose=p;addSceneObject(this);}
    
    Robot(String n, ScenePoint p, float d) {name=n;pose=new Pose(p,d);addSceneObject(this);}
  
    void set(ScenePoint p, float d) {pose=new Pose(p,d);}
  
    void set(Pose p) {pose=p;}
  
  //TODO: write method to run motorcommands(mayby this is where ROS publishes)
    void run() {
      ScreenPoint p=pose::position.toScreenPoint();
      float sr=toScreenUnit(diameter/2);
      stroke(0);
      strokeWeight(2);
      fill(col);
      ellipse(p::x, p::y,
              2*sr, 2*sr);
      float sinDir=sin(radians(pose::direction)); 
      float cosDir=cos(radians(pose::direction));
      
      if(overlappingOther()) drawWarningFrame();
      if(runaway()) {drawWarningFrame();drawWarningOnEdges();}
      
      
    }
  
  //  void moveTo(Pose p) {pose=p;}
  
    bool hasInside(ScenePoint sp) {
      float x=pose::position::x; float y=pose::position::y;
      return x-diameter/2<=sp::x && sp::x<=x+diameter/2 && y-diameter/2<=sp::y && sp::y<=y+diameter/2;
    }
      
    bool overlappingOther() {
      float x=pose::position::x; float y=pose::position::y;
      float r=diameter/2;
      boolean result=false;
      for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i]!=this) {
        if( allSceneObjects[i].hasInside(p(x+r,y+r)) ) result=true;
        if( allSceneObjects[i].hasInside(p(x-r,y+r)) ) result=true;
        if( allSceneObjects[i].hasInside(p(x+r,y-r)) ) result=true;
        if( allSceneObjects[i].hasInside(p(x-r,y-r)) ) result=true;
      } 
      return result;
    }
    
    boolean runaway() {
      float x=pose::position::x; float y=pose::position::y;
      float r=diameter/2;
      boolean result = false;
      if(p(x+r,y+r).runaway()) result=true;
      if(p(x-r,y+r).runaway()) result=true;
      if(p(x+r,y-r).runaway()) result=true;
      if(p(x-r,y-r).runaway()) result=true;
      return result;
    }
    
    void publishWarningFrame() {
      cout << n + " collision";
    } 
  
    void publishWarningOnEdges() {
      cout << n + " has left the building";
    }
};
// easy constructors
Robot robot(String n) {return new Robot(n);}
Robot robot(String n, Pose p) {return new Robot(n, p);}
Robot robot(String n, ScenePoint p, float d) {return new Robot(n, p, d);}
