#include "SceneObject.cpp"
//#include "Pose.cpp"
#include <string>
#include <iostream>

using namespace std;

class Robot : public SceneObject {
  public:
    Robot(string t);
    Robot(string t, Pose p);
    Robot(string t, ScenePoint p, float d);
    Robot(){};
    ~Robot();
    Robot robot(string t);
    Robot robot(string t, Pose p);
    Robot robot(string t, ScenePoint p, float d);
    bool operator==(Robot r);
    void set(ScenePoint p, float d);
    void set(Pose p);
    //TODO: write method to run motorcommands(mayby this is where ROS publishes)
    void run();  
    //  void moveTo(Pose p) {pose=p;}  
    bool hasInside(ScenePoint sp);
    bool overlappingOther();
    bool runaway();
    void publishWarningFrame();
    void publishWarningOnEdges();
//  private:
    Pose pose;
    float diameter; //meters
    float maxTurn; // degrees; this version: the same for all robots
    float maxSpeed; // m/sec; this version: the same for all robots
};

Robot::Robot(string t) {
  topic=t;
  addSceneObject(*this);
  diameter = 0.3; //meters
  maxTurn=35; // degrees; this version: the same for all robots
  maxSpeed= 1; // m/sec; this version: the same for all robots
}

Robot::Robot(string t, Pose p) {
  topic=t;
  pose=p;
  addSceneObject(*this);
  diameter = 0.3; //meters
  maxTurn=35; // degrees; this version: the same for all robots
  maxSpeed= 1; // m/sec; this version: the same for all robots
}

Robot::Robot(string t, ScenePoint p, float d) {
  topic=t;
  pose=Pose(p,d);
  addSceneObject(*this);
  diameter = 0.3; //meters
  maxTurn=35; // degrees; this version: the same for all robots
  maxSpeed= 1; // m/sec; this version: the same for all robots
}

// easy constructors
Robot Robot::robot(string t) {return Robot(t);}
Robot Robot::robot(string t, Pose p) {return Robot(t, p);}
Robot Robot::robot(string t, ScenePoint p, float d) {return Robot(t, p, d);}

bool Robot::operator==(Robot r){
  if(topic == r.topic && pose == r.pose && diameter == r.diameter && maxTurn == r.maxTurn && maxSpeed == r.maxSpeed){
    return true;
  }
  return false;
}

void Robot::set(ScenePoint p, float d) {pose = Pose(p,d);}
void Robot::set(Pose p) {pose=p;}

void Robot::run() {
  /*ScreenPoint p=pose::position.toScreenPoint();
  float sr=toScreenUnit(diameter/2);
  stroke(0);
  strokeWeight(2);
  fill(col);
  ellipse(p::x, p::y, 2*sr, 2*sr);
  float sinDir=sin(radians(pose::direction)); 
  float cosDir=cos(radians(pose::direction));
  if(overlappingOther()) drawWarningFrame();
  if(runaway()) {drawWarningFrame();drawWarningOnEdges();}
  */      
}

bool Robot::hasInside(ScenePoint sp) {
  float x=pose.position.x; float y=pose.position.y;
  return x-diameter/2<=sp.x && sp.x<=x+diameter/2 && y-diameter/2<=sp.y && sp.y<=y+diameter/2;
}

bool Robot::overlappingOther() {
  float x=pose.position.x; float y=pose.position.y;
  Scene s=pose.scene;
  float r=diameter/2;
  bool result=false;
  for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i]!=this) {
    if( allSceneObjects[i]->hasInside(p(s, x+r,y+r)) ) result=true;
    if( allSceneObjects[i]->hasInside(p(s, x-r,y+r)) ) result=true;
    if( allSceneObjects[i]->hasInside(p(s, x+r,y-r)) ) result=true;
    if( allSceneObjects[i]->hasInside(p(s, x-r,y-r)) ) result=true;
 } 
 return result;
}

bool Robot::runaway() {
  Scene s=pose.scene;
  float x=pose.position.x; float y=pose.position.y;
  float r=diameter/2;
  bool result = false;
  if(p(s, x+r,y+r).runaway()) result=true;
  if(p(s, x-r,y+r).runaway()) result=true;
  if(p(s, x+r,y-r).runaway()) result=true;
  if(p(s, x-r,y-r).runaway()) result=true;
  return result;
}

void Robot::publishWarningFrame() {
  cout << topic + " collision";
} 

void Robot::publishWarningOnEdges() {
  cout << topic + " has left the building";
}

