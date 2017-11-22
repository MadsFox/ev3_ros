#pragma once
#include <vector>
#include "Robot.cpp"
#include <iostream>

using namespace std;

float epsilon = 0.01; // 1 cm

class Route {  // find bedre navn
  public:
    Route(Robot r, int n, vector<Pose> pp, float td);
    Route(){};
    ~Route();
    string getType();
    bool operator==(Route r);
    friend Route forwardRoute(Robot robot, Pose from, Pose to);
    friend Route mkBackwardRouteFromBotheEndsINTERNAL(Robot robot, Pose from, Pose to);
    friend Route backwardRoute(Robot robot, Pose from, Pose to);
    friend Route forwardTurnLeftRoute(Robot robot, Pose p, float radius, float angle);
    friend Route forwardTurnRightRoute(Robot robot, Pose p, float radius, float angle);
    friend Route backwardTurnLeftRoute(Robot robot, Pose p, float radius, float angle);
    friend Route backwardTurnRightRoute(Robot robot, Pose p, float radius, float angle);
//  private:
    Robot robot;
    int noOfSteps;
    vector<Pose> poses; // no assumptions here about speed
    float travelDist;  // in metres; will only be approximate
      
    //Route(Pose from, Pose to) {
    //    Route r=NULL;
    //    r= forwardRoute(from,to);
    //    if(r==NULL){
    //      println("Route("+from+", "+to+") too complicated; try something else!!!!!!!!!!!!!!!!");
    //      System.exit(1);
    //      noOfSteps=0; poses=NULL; noOfSteps=0;}
    //    else{noOfSteps=r.noOfSteps; poses=r.poses;}
    //}
};

Route::Route(Robot r, int n, vector<Pose> pp, float td) {robot=r;noOfSteps=n; poses=pp; travelDist=td;}

string Route::getType(){
  return "Route";
}

bool Route::operator==(Route r){
  bool equal = false;;
  if(robot == r.robot && noOfSteps == r.noOfSteps && poses.size() == r.poses.size() && travelDist == r.travelDist){
    for(int i = 0; i < poses.size(); i++){
      if(poses.at(i) == r.poses.at(i)){
        equal = true;
      }else{
        equal = false;
        return equal;
      }
    }
  }
  return equal;
}

Route forwardRoute(Robot robot, Pose from, Pose to) {
  float travelDist = 0;
  vector<Pose> firstHalf;
  vector<Pose> lastHalf;
  
  // catch infinite loops:
  int pathLength=1;
  
  Pose currentFrom=from; Pose currentTo=to;
  while(dist(currentFrom,currentTo)>=2*epsilon && pathLength<100000) {
    pathLength+=2;
    Pose station1; float bestDist=10000000;
    for(int k=0; k<=101; k++) {  // use odd number (100+1) so "straight ahead" is also an option
      Pose suggest = currentFrom.klone();
      suggest.moveRelPhiD(-robot.maxTurn+float(k)/101*2*robot.maxTurn,epsilon);
      float suggestDist = dist(suggest,currentTo);
      if(suggestDist<bestDist) {bestDist=suggestDist;station1=suggest;}
    }
    firstHalf.push_back(station1); travelDist+=epsilon; 
    currentFrom=station1;
    lastHalf.push_back(currentTo);
    
    Pose stationN; bestDist=10000000;
    for(int k=0; k<=101; k++) {  // use odd number (100+1) so "straight ahead" is also an option
      Pose suggest = currentTo.klone();
      suggest.moveRelPhiD(-robot.maxTurn+float(k)/101*2*robot.maxTurn,-epsilon); // break symmetry by change of direction                                                         
      float suggestDist = dist(suggest,currentFrom);
      if(suggestDist<bestDist) {bestDist=suggestDist;stationN=suggest;}
    }
    currentTo=stationN; travelDist+=epsilon; 
  }
  
  Pose allPoses[firstHalf.size()+lastHalf.size()+1];
  for(int i=0; i<firstHalf.size(); i++) {allPoses[i]=firstHalf[i];}
  allPoses[firstHalf.size()] = avgPose(currentFrom.scene, currentFrom,currentTo); travelDist=dist(from,to);
  for(int i=0; i<lastHalf.size(); i++) allPoses[firstHalf.size()+lastHalf.size()-i]=lastHalf[i];
  
  
  
  if(pathLength>=100000) {
    cout << "Route(" << from.toString() << ", " << to.toString() << ") too complicated; try something else";
    exit(EXIT_FAILURE); }
  vector<Pose> ap(allPoses, allPoses + sizeof allPoses / sizeof allPoses[0]);
  return Route(robot, sizeof(allPoses),ap,travelDist);
  /// TEST AND MAKE A WARNING IF travelDist >> robotTurningDiameter*PI + dist(from,to)
}
////////////////////////////////////////////////////////////end
////////////////////////////////////////////////////////////

Route mkBackwardRouteFromBotheEndsINTERNAL(Robot robot, Pose from, Pose to) {
  Route r = forwardRoute(robot, to, from);
  Route ro;
  if(r==ro) return ro;
  // reverse
  int m= r.noOfSteps/2; if(r.noOfSteps/2*2==r.noOfSteps) m+=1; 
  for(int i=0; i<m; i++) {
    Pose p=r.poses[i];
    r.poses[i] = r.poses[r.noOfSteps-i-2];
    r.poses[r.noOfSteps-i-1]=p;
  }
  r.poses[r.noOfSteps-1]=to;
  return r;
}

Route backwardRoute(Robot robot, Pose from, Pose to) {
  Route r;
  r= mkBackwardRouteFromBotheEndsINTERNAL(robot, from,to);
  Route ro;
  if(r==ro){
    cout << "Route(" << from.toString() << ", " << to.toString() << ") too complicated; try something else";
    exit(EXIT_FAILURE); 
  } 
  return r;
}

Route forwardTurnLeftRoute(Robot robot, Pose p, float radius, float angle) {
 Pose center=p.klone();
 center.moveRelXRelY(-cos(2*M_PI*p.direction/360)*radius, sin(2*M_PI*p.direction/360)*radius);
 float phi0 = normalizeAngle(p.direction+90);
 float travelLength = radius*2*M_PI*angle/360;
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 - (i+1)*angle/noOfSteps);
   poses[i] = Pose(p.scene, center.x+sin(2*M_PI*phi/360)*radius, center.y+cos(2*M_PI*phi/360)*radius, normalizeAngle(phi-90));
 }
 vector<Pose> ps(poses, poses + sizeof poses / sizeof poses[0]);
 return Route(robot, sizeof(poses),ps,travelLength);
}


Route forwardTurnRightRoute(Robot robot, Pose p, float radius, float angle) {
 Pose center=p.klone();
 center.moveRelXRelY(cos(2*M_PI*p.direction/360)*radius, -sin(2*M_PI*p.direction/360)*radius);
 float phi0 = normalizeAngle(p.direction-90);
 float travelLength = radius*2*M_PI*angle/360;
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 + (i+1)*angle/noOfSteps);
   poses[i] = Pose(p.scene, center.x+sin(2*M_PI*phi/360)*radius, center.y+cos(2*M_PI*phi/360)*radius, normalizeAngle(phi-90));
 }
 vector<Pose> ps(poses, poses + sizeof poses / sizeof poses[0]);
 return Route(robot, sizeof(poses),ps,travelLength);}


Route backwardTurnLeftRoute(Robot robot, Pose p, float radius, float angle) {
 Pose center=p.klone();
 center.moveRelXRelY(-cos(2*M_PI*p.direction/360)*radius, sin(2*M_PI*p.direction/360)*radius);
 float phi0 = normalizeAngle(p.direction+90);
 float travelLength = radius*2*M_PI*angle/360;
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 + (i+1)*angle/noOfSteps);
   poses[i] = Pose(p.scene, center.x+sin(2*M_PI*phi/360)*radius, center.y+cos(2*M_PI*phi/360)*radius, normalizeAngle(phi-90));
 }
 vector<Pose> ps(poses, poses + sizeof poses / sizeof poses[0]);
 return Route(robot, sizeof(poses),ps,travelLength);
}

Route backwardTurnRightRoute(Robot robot, Pose p, float radius, float angle) {
 Pose center=p.klone();
 center.moveRelXRelY(cos(2*M_PI*p.direction/360)*radius, -sin(2*M_PI*p.direction/360)*radius);
 float phi0 = normalizeAngle(p.direction-90);
 float travelLength = radius*2*M_PI*angle/360;
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 - (i+1)*angle/noOfSteps);
   poses[i] = Pose(p.scene, center.x+sin(2*M_PI*phi/360)*radius, center.y+cos(2*M_PI*phi/360)*radius, normalizeAngle(phi-90));
 }
 vector<Pose> ps(poses, poses + sizeof poses / sizeof poses[0]);
 return Route(robot, sizeof(poses),ps,travelLength);}
