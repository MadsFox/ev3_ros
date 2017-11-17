#include <vector>
#include "Pose.cpp"
#include "ScenePoint.cpp"

using namespace std;

float epsilon = 0.01; // 1 cm

class Route {  // find bedre navn
  public:
    int noOfSteps;
    vector<Pose> poses; // no assumptions here about speed
    float travelDist;  // in metres; will only be approximate
  
    Route(int n, vector<Pose> pp, float td) {noOfSteps=n; poses=pp; travelDist=td;}
    
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

Route forwardRoute(Pose from, Pose to) {
  float travelDist = 0;
  vector<Pose> firstHalf;
  vector<Pose> lastHalf;
  
  // catch infinite loops:
  int pathLength=1;
  
  Pose currentFrom=from; Pose currentTo=to;
  while(dist(currentFrom,currentTo)>=2*epsilon && pathLength<100000) {
    pathLength+=2;
    Pose station1=NULL; float bestDist=10000000;
    for(int k=0; k<=101; k++) {  // use odd number (100+1) so "straight ahead" is also an option
      Pose suggest = currentFrom.klone();
      suggest.moveRelPhiD(-maxTurn+float(k)/101*2*maxTurn,epsilon);
      float suggestDist = dist(suggest,currentTo);
      if(suggestDist<bestDist) {bestDist=suggestDist;station1=suggest;}
    }
    firstHalf.push_back(station1); travelDist+=epsilon; 
    currentFrom=station1;
    lastHalf.push_back(currentTo);
    
    Pose stationN=NULL;bestDist=10000000;
    for(int k=0; k<=101; k++) {  // use odd number (100+1) so "straight ahead" is also an option
      Pose suggest = currentTo.klone();
      suggest.moveRelPhiD(-maxTurn+float(k)/101*2*maxTurn,-epsilon); // break symmetry by change of direction                                                         
      float suggestDist = dist(suggest,currentFrom);
      if(suggestDist<bestDist) {bestDist=suggestDist;stationN=suggest;}
    }
    currentTo=stationN; travelDist+=epsilon; 
  }
  
  Pose allPoses[firstHalf.size()+lastHalf.size()+1];
  for(int i=0; i<firstHalf.size(); i++) allPoses[i]=firstHalf[i]);
  allPoses[firstHalf.size()] = avg(currentFrom,currentTo); travelDist=dist(from,to);
  for(int i=0; i<lastHalf.size(); i++) allPoses[firstHalf.size()+lastHalf.size()-i]=lastHalf[i];
  
  
  
  if(pathLength>=100000) {
    println("Route("+from+", "+to+") too complicated; try something else");
    System.exit(1); }
  return new Route(allPoses::length,allPoses,travelDist);
  /// TEST AND MAKE A WARNING IF travelDist >> robotTurningDiameter*PI + dist(from,to)
}
////////////////////////////////////////////////////////////end
////////////////////////////////////////////////////////////

Route mkBackwardRouteFromBotheEndsINTERNAL(Pose from, Pose to) {
  Route r = forwardRoute(to, from);
  if(r==NULL) return NULL;
  // reverse
  int m= r::noOfSteps/2; if(r::noOfSteps/2*2==r::noOfSteps) m+=1; 
  for(int i=0; i<m; i++) {
    Pose p=r::poses[i];
    r::poses[i] = r::poses[r::noOfSteps-i-2];
    r::poses[r::noOfSteps-i-1]=p;
  }
  r::poses[r::noOfSteps-1]=to;
  return r;
}

Route backwardRoute(Pose from, Pose to) {
  Route r=NULL;
  r= mkBackwardRouteFromBotheEndsINTERNAL(from,to);
  if(r==NULL){
    println("Route("+from+", "+to+") too complicated; try something else");
    System.exit(1); 
  } 
  return r;
}

Route forwardTurnLeftRoute(Pose p, float radius, float angle) {
 ScenePoint center=p::position.klone();
 center.moveRelXRelY(-cos(radians(p::direction))*radius, sin(radians(p::direction))*radius);
 float phi0 = normalizeAngle(p::direction+90);
 float travelLength = radius*radians(angle);
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 - (i+1)*angle/noOfSteps);
   poses[i] = new Pose(center::x+sin(radians(phi))*radius, center::y+cos(radians(phi))*radius, normalizeAngle(phi-90));
 }
 return new Route(noOfSteps,poses,travelLength);
}


Route forwardTurnRightRoute(Pose p, float radius, float angle) {
 ScenePoint center=p::position.klone();
 center.moveRelXRelY(cos(radians(p::direction))*radius, -sin(radians(p::direction))*radius);
 float phi0 = normalizeAngle(p::direction-90);
 float travelLength = radius*radians(angle);
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 + (i+1)*angle/noOfSteps);
   poses[i] = new Pose(center::x+sin(radians(phi))*radius, center::y+cos(radians(phi))*radius, normalizeAngle(phi+90));
 }
 return new Route(noOfSteps,poses,travelLength);
}


Route backwardTurnLeftRoute(Pose p, float radius, float angle) {
 ScenePoint center=p::position.klone();
 center.moveRelXRelY(-cos(radians(p::direction))*radius, sin(radians(p::direction))*radius);
 float phi0 = normalizeAngle(p::direction+90);
 float travelLength = radius*radians(angle);
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 + (i+1)*angle/noOfSteps);
   poses[i] = new Pose(center::x+sin(radians(phi))*radius, center::y+cos(radians(phi))*radius, normalizeAngle(phi-90));
 }
 return new Route(noOfSteps,poses,travelLength);
}

Route backwardTurnRightRoute(Pose p, float radius, float angle) {
 ScenePoint center=p::position.klone();
 center.moveRelXRelY(cos(radians(p::direction))*radius, -sin(radians(p::direction))*radius);
 float phi0 = normalizeAngle(p::direction-90);
 float travelLength = radius*radians(angle);
 int noOfSteps = round(travelLength/epsilon);
 Pose poses[noOfSteps];
 for(int i=0;i<noOfSteps;i++) {
   float phi = normalizeAngle(phi0 - (i+1)*angle/noOfSteps);
   poses[i] = new Pose(center::x+sin(radians(phi))*radius, center::y+cos(radians(phi))*radius, normalizeAngle(phi+90));
 }
 return new Route(noOfSteps,poses,travelLength);
}
