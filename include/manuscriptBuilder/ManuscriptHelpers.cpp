#include "Route.cpp"
#include "Event.cpp"

// manuscript writing time information

Pose mostRecentRecordedPose[100]; // enough

void initialPose(Robot r, Pose p) {
  // maintain manuscript writing time information
  mostRecentRecordedPose[indexOf(r)]=p;  //crashes if robot not present
  // maintain internal reresentation of script;
  new Event(0,r,p);
}


void moveTo(Robot r, float startTime, Pose to) {
  Route route = forwardRoute(mostRecentRecordedPose[indexOf(r)], to);
  mostRecentRecordedPose[indexOf(r)]=to;
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) new Event(startTime+float(i)/50,r,route.poses[i]);
}

void moveTo(Robot r, Pose to) {moveTo(r,timeOfLastGeneratedEvent(r),to);}

void moveTo(Robot r, float x, float y, float phi) {moveTo(r, new Pose(x,y,phi));}

void moveTo(Robot r, Pose via, Pose to) {moveTo(r,via);moveTo(r,to);}

void moveTo(Robot r, Pose via1, Pose via2, Pose to) {moveTo(r,via1);moveTo(r,via2);moveTo(r,to);}

void moveTo(Robot r, Pose via1, Pose via2, Pose via3, Pose to) {moveTo(r,via1);moveTo(r,via2);moveTo(r,via3);moveTo(r,to);}

void moveTo(Robot r, float x1, float y1, float phi1,
                     float x2, float y2, float phi2,
                     float x, float y, float phi)
   {moveTo(r, new Pose(x1,y1,phi1));moveTo(r, new Pose(x2,y2,phi2));moveTo(r, new Pose(x,y,phi));}

void moveTo(Robot r, float x1, float y1, float phi1,
                     float x, float y, float phi)
   {moveTo(r, new Pose(x1,y1,phi1));moveTo(r, new Pose(x,y,phi));}


void moveToBacking(Robot r, float startTime, Pose to) {
  // returns arrival time
  Route route = backwardRoute(mostRecentRecordedPose[indexOf(r)], to);
  mostRecentRecordedPose[indexOf(r)]=to;
  // arbitrary speed in this version
  for(int i=0;i<route.noOfSteps;i++) new Event(startTime+float(i)/50,r,route::poses[i]);
}

void moveToBacking(Robot r, Pose to) {moveToBacking(r,timeOfLastGeneratedEvent(r),to);}

void moveToBacking(Robot r, float x, float y, float phi) {moveToBacking(r, new Pose(x,y,phi));}

void moveToBacking(Robot r, Pose via, Pose to) {moveToBacking(r,via);moveTo(r,to);}

void moveToBacking(Robot r, Pose via1, Pose via2, Pose to) {moveToBacking(r,via1);moveToBacking(r,via2);moveToBacking(r,to);}

void moveToBacking(Robot r, Pose via1, Pose via2, Pose via3, Pose to) {moveToBacking(r,via1);moveToBacking(r,via2);moveToBacking(r,via3);moveToBacking(r,to);}

void moveToBacking(Robot r, float x1, float y1, float phi1,
                     float x2, float y2, float phi2,
                     float x, float y, float phi)
   {moveToBacking(r, new Pose(x1,y1,phi1));moveToBacking(r, new Pose(x2,y2,phi2));moveToBacking(r, new Pose(x,y,phi));}

void moveToBacking(Robot r, float x1, float y1, float phi1,
                     float x, float y, float phi)
   {moveToBacking(r, new Pose(x1,y1,phi1));moveToBacking(r, new Pose(x,y,phi));}

void wait(Robot r, float waitingTime) {
  new Event(timeOfLastGeneratedEvent(r),r, waitingTime);
}

void circleLeft(Robot r,float radius, float angle) {circleLeft(r,timeOfLastGeneratedEvent(r),radius,angle);}

void circleLeft(Robot r,float startTime,float radius, float angle) {
  Route route = forwardTurnLeftRoute(mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route::poses[route::poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route::noOfSteps;i++) new Event(startTime+float(i)/50,r,route::poses[i]);
}

void circleRight(Robot r,float radius, float angle) {circleRight(r,timeOfLastGeneratedEvent(r),radius,angle);}

void circleRight(Robot r,float startTime,float radius, float angle) {
  Route route = forwardTurnRightRoute(mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route::poses[route::poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route::noOfSteps;i++) new Event(startTime+float(i)/50,r,route::poses[i]);
}

void circleLeftBacking(Robot r,float radius, float angle) {circleLeftBacking(r,timeOfLastGeneratedEvent(r),radius,angle);}

void circleLeftBacking(Robot r,float startTime,float radius, float angle) {
  Route route = backwardTurnLeftRoute(mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route::poses[route::poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route::noOfSteps;i++) new Event(startTime+float(i)/50,r,route::poses[i]);
}

void circleRightBacking(Robot r,float radius, float angle) {circleRightBacking(r,timeOfLastGeneratedEvent(r),radius,angle);}

void circleRightBacking(Robot r,float startTime,float radius, float angle) {
  Route route = backwardTurnRightRoute(mostRecentRecordedPose[indexOf(r)], radius, angle);
  mostRecentRecordedPose[indexOf(r)]=route::poses[route::poses.size()-1];
  // arbitrary speed in this version
  for(int i=0;i<route::noOfSteps;i++) new Event(startTime+float(i)/50,r,route::poses[i]);
}

void synchronize() {
  // all wait until slowest one up done its tasks
  float synchTime = timeOfLastGeneratedEvent();
  for(int i=0;i<allSceneObjects.size();i++)
    if(allSceneObjects[i] instanceof Robot)
      wait((Robot)allSceneObjects[i], synchTime - timeOfLastGeneratedEvent((Robot)allSceneObjects[i]));
}

void synchronize(Robot r1, Robot r2) {
  //!!!!!!!! VERY LAZY - NOT IMPLEMENTED; WORKS ONLY FOR AN EXAMPLE WITH AXACTLY TWO ROBOTS ON STAGE!!!
  // all wait until slowest one up done its tasks
  float synchTime = timeOfLastGeneratedEvent();
  for(int i=0;i<allSceneObjects.size();i++)
    if(allSceneObjects[i] instanceof Robot)
      wait((Robot)allSceneObjects[i], synchTime - timeOfLastGeneratedEvent((Robot)allSceneObjects[i]));
}
