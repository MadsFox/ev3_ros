#include "Route.cpp"
#include "Event.cpp"

// manuscript writing time information

namespace manuscript_helpers{

Scene s;

//Pose mostRecentRecordedPose[100]; // enough
vector<Pose> mostRecentRecordedPose;
void initScene(float width, float depth){
  s = new Scene(width, depth);
}

void initialPose(Robot r, Pose p) {
  // maintain manuscript writing time information
  mostRecentRecordedPose[indexOf(r)]=p;  //crashes if robot not present
  // maintain internal reresentation of script;
  Event(0,r,p);
}

void initialPose(Robot r, float x, float y, float d) {
  Pose p = pose(s, x, y, d);
  // maintain manuscript writing time information
  mostRecentRecordedPose[indexOf(r)]=p;  //crashes if robot not present
  // maintain internal reresentation of script;
  Event(0,r,p);
}

void initialPose(string name, float x, float y, float d) {
  Pose p = Pose(s, x, y, d);
  Robot r = Robot(name);
  // maintain manuscript writing time information
  mostRecentRecordedPose.insert(mostRecentRecordedPose.begin()+indexOf(r), p);  //crashes if robot not present
//  mostRecentRecordedPose[indexOf(Robot(name))]=Pose(s, x, y, d);  //crashes if robot not present

  // maintain internal reresentation of script;
  Event(0,r,p);
}

void moveTo(Robot r, float startTime, Pose to) {
  Route route = forwardRoute(r, mostRecentRecordedPose[indexOf(r)], to);
  mostRecentRecordedPose[indexOf(r)]=to;
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) Event(startTime+float(i)/50,r,route.poses[i]);
}

void moveTo(string name, Pose to) {
  Robot r = Robot(name);  
  moveTo(r,timeOfLastGeneratedEvent(r),to);}

void moveTo(string name, float x, float y, float phi) {moveTo(name, Pose(s,x,y,phi));}

void moveTo(string name, Pose via, Pose to) {moveTo(name,via);moveTo(name,to);}

void moveTo(string name, Pose via1, Pose via2, Pose to) {moveTo(name,via1);moveTo(name,via2);moveTo(name,to);}

void moveTo(string name, Pose via1, Pose via2, Pose via3, Pose to) {
  moveTo(name,via1);moveTo(name,via2);moveTo(name,via3);moveTo(name,to);}

void moveTo(string name, float x1, float y1, float phi1,
                         float x2, float y2, float phi2,
                         float x, float y, float phi)
   {moveTo(name, Pose(s,x1,y1,phi1));moveTo(name, Pose(s,x2,y2,phi2));moveTo(name, Pose(s,x,y,phi));}

void moveTo(string name, float x1, float y1, float phi1,
                         float x, float y, float phi)
   {moveTo(name, Pose(s,x1,y1,phi1));moveTo(name, Pose(s,x,y,phi));}


void moveToBacking(string name, float startTime, Pose to) {
  Robot r = Robot(name);
  // returns arrival time
  Route route = backwardRoute(r, mostRecentRecordedPose[indexOf(r)], to);
  mostRecentRecordedPose[indexOf(r)]=to;
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) Event(startTime+float(i)/50,r,route.poses[i]);
}

void moveToBacking(string name, Pose to) {
  Robot r = Robot(name);
  moveToBacking(name,timeOfLastGeneratedEvent(r),to);}

void moveToBacking(string name, float x, float y, float phi) {moveToBacking(name, Pose(s,x,y,phi));}

void moveToBacking(string name, Pose via, Pose to) {moveToBacking(name,via);moveTo(name,to);}

void moveToBacking(string name, Pose via1, Pose via2, Pose to) {
  moveToBacking(name,via1);moveToBacking(name,via2);moveToBacking(name,to);}

void moveToBacking(string name, Pose via1, Pose via2, Pose via3, Pose to) {
  moveToBacking(name,via1);moveToBacking(name,via2);moveToBacking(name,via3);moveToBacking(name,to);}

void moveToBacking(string name, float x1, float y1, float phi1,
                                float x2, float y2, float phi2,
                                float x, float y, float phi)
   {moveToBacking(name, Pose(s,x1,y1,phi1));moveToBacking(name, Pose(s,x2,y2,phi2));moveToBacking(name, Pose(s,x,y,phi));}

void moveToBacking(string name, float x1, float y1, float phi1,
                                float x, float y, float phi)
   {moveToBacking(name, Pose(s,x1,y1,phi1));moveToBacking(name, Pose(s,x,y,phi));}

void wait(string name, float waitingTime) {
  Robot r = Robot(name);
  Event(timeOfLastGeneratedEvent(r),r, waitingTime);
}

void circleLeft(string name,float startTime,float radius, float angle) {
  Robot r = Robot(name);
  Route route = forwardTurnLeftRoute(r, mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route.poses[route.poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) Event(startTime+float(i)/50,r,route.poses[i]);
}

void circleLeft(string name, float radius, float angle) {
  Robot r = Robot(name);  
  circleLeft(name,timeOfLastGeneratedEvent(r),radius,angle);}

void circleRight(Robot r, float startTime,float radius, float angle) {
  Route route = forwardTurnRightRoute(r, mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route.poses[route.poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) Event(startTime+float(i)/50,r,route.poses[i]);
}

void circleRight(string name, float radius, float angle) {
  Robot r = Robot(name);    
  circleRight(r,timeOfLastGeneratedEvent(r),radius,angle);}

void circleLeftBacking(Robot r, float startTime,float radius, float angle) {
  Route route = backwardTurnLeftRoute(r, mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route.poses[route.poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) Event(startTime+float(i)/50,r,route.poses[i]);
}

void circleLeftBacking(string name,float radius, float angle) {
  Robot r = Robot(name);  
  circleLeftBacking(r,timeOfLastGeneratedEvent(r),radius,angle);}

void circleRightBacking(Robot r,float startTime,float radius, float angle) {
  Route route = backwardTurnRightRoute(r, mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route.poses[route.poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) Event(startTime+float(i)/50,r,route.poses[i]);
}

void circleRightBacking(string name, float radius, float angle) {
  Robot r = Robot(name);
  circleRightBacking(r,timeOfLastGeneratedEvent(r),radius,angle);}

void synchronize() {
  // all wait until slowest one up done its tasks
  float synchTime = timeOfLastGeneratedEvent();
  for(int i=0;i<allSceneObjects.size();i++){
    if(allSceneObjects[i]->getType() == "Robot"){
      wait(allSceneObjects[i]->topic, synchTime - timeOfLastGeneratedEvent(allSceneObjects[i]->topic));
    }
  }
}

void synchronize(Robot r1, Robot r2) {
  //!!!!!!!! VERY LAZY - NOT IMPLEMENTED; WORKS ONLY FOR AN EXAMPLE WITH AXACTLY TWO ROBOTS ON STAGE!!!
  // all wait until slowest one up done its tasks
  float synchTime = timeOfLastGeneratedEvent();
  for(int i=0;i<allSceneObjects.size();i++)
    if(allSceneObjects[i]->getType() == "Robot")
      wait(allSceneObjects[i]->topic, synchTime - timeOfLastGeneratedEvent(allSceneObjects[i]->topic));
}
/*void endShow(){
/*  for(int i=0; i<100; i++){
    delete[] mostRecentRecordedPose[i];
  }
  delete mostRecentRecordedPose;
}*/
}
