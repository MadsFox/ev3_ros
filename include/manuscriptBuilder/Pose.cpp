#pragma once
#include "ScenePoint.cpp"
#define _USE_MATH_DEFINES
#include <math.h>
#include <string>
#include <sstream>
//#include <stdlib.h>
#include <cmath>

using namespace std;

class Pose : public ScenePoint {// for a robot
  public:
    //Class methods
    Pose klone();// intuitively same as clone, but returns object of right class
    string toString();
    string getType();
    void moveRelPhiD(float deltaPhi, float deltaDist);  
    void moveAbsPhiD(float phi, float deltaDist);
    bool operator==(Pose po);
    friend Pose pose(Scene scene, float x, float y, float d);
    friend Pose avgPose(Scene scene, Pose p1, Pose p2);
    friend float normalizeAngle(float phi);
    friend float normalizeAngleRad(float phi);
    friend float dist(Pose p1, Pose p2);
    friend float dist(Pose p1, ScenePoint p2);
    friend float dist(ScenePoint p1, Pose p2);
    //Constructors
    Pose(Scene _scene, float xx, float yy, float dd);
    Pose(ScenePoint ss, float dd);
    Pose(){};
    ~Pose();
//  private:
    Scene scene;
    ScenePoint position; 
    float direction; // 0..360;
    
    // directions internally in degrees; memotech. as n,e,s,w etc.
    // south means looking out of from scene towards audience
    float north;// = 0;
    float east;// = 90;
    float south;// = 180;
    float west;// = 270;
    float northEast;// = north+90/2;
    float southEast;// = south-90/2;
    float northWest;//=west+90/2;
    float southWest;//=west-90/2;
    float nne;//=north+90/4;
    float ene;//=east-90/4;
    float ese;//=east+90/4;
    float sse;//=south-90/4;
    float ssw;//=south+90/4;
    float wsw;//=west-90/4;
    float wnw;//=west+90/4;
    float nnw;//=360-90/4;

    float robotTurningDiameter;// = 0.7;
    // Currently only used for checking feasibility of generated route
    // in mkXXXXXRouteXXXX; should be correlated with constant epsilon and expected robot diameter
};

Pose::Pose(Scene _scene, float xx, float yy, float dd) {
  position = ScenePoint(_scene,xx,yy); direction=dd;
  north = 0;
  east = 90;
  south = 180;
  west = 270;
  northEast = north+90/2;
  southEast = south-90/2;
  northWest=west+90/2;
  southWest=west-90/2;
  nne=north+90/4;
  ene=east-90/4;
  ese=east+90/4;
  sse=south-90/4;
  ssw=south+90/4;
  wsw=west-90/4;
  wnw=west+90/4;
  nnw=360-90/4;
  robotTurningDiameter = 0.7;
}

Pose::Pose(ScenePoint ss, float dd) {
  position = ss; direction=dd;
  north = 0;
  east = 90;
  south = 180;
  west = 270;
  northEast = north+90/2;
  southEast = south-90/2;
  northWest=west+90/2;
  southWest=west-90/2;
  nne=north+90/4;
  ene=east-90/4;
  ese=east+90/4;
  sse=south-90/4;
  ssw=south+90/4;
  wsw=west-90/4;
  wnw=west+90/4;
  nnw=360-90/4;
  robotTurningDiameter = 0.7;
}

Pose Pose::klone() {return Pose(ScenePoint(position),direction);} // intuitively same as clone, but returns object of right class

string Pose::toString() {
  ostringstream stm;
  stm << position.toString() << "*phi=" << direction;
  return stm.str();  
}

string Pose::getType(){
  return "Pose";
}

void Pose::moveRelPhiD(float deltaPhi, float deltaDist) {
  // phi added to current direction, but scaled by deltaDist AND SOME CONSTANT THAT DEPENDS ON PHYSICAL DETAILS OF THE ROBOT
  moveAbsPhiD(direction+deltaPhi*abs(deltaDist)*4,deltaDist);
}

float normalizeAngle(float phi) {if(phi<0)return normalizeAngle(phi+360);else if(phi>=360)return normalizeAngle(phi-360); else return phi;}
float normalizeAngleRad(float phi) {if(phi<0)return normalizeAngle(phi+2*M_PI);else if(phi>=2*M_PI)return normalizeAngle(phi-2*M_PI); else return phi;}


void Pose::moveAbsPhiD(float phi, float deltaDist) {
  // set new direction and move
  direction=normalizeAngle(phi);
  position.moveRelPhiD(direction,deltaDist);
}

bool Pose::operator==(Pose po){
  if(position == po.position && direction == po.direction){
    return true;
  }
  return false;
}    

// easy constructor:
Pose pose(Scene scene, float x, float y, float d) {return Pose(scene, x,y,d);}

Pose avgPose(Scene scene, Pose p1, Pose p2) {
  return Pose(avg(scene, p1.position,p2.position),(p1.direction+p2.direction)/2);
}

float dist(Pose p1, Pose p2) {
  // plain euclidian, ignoring direction
  return dist(p1.position, p2.position);
}
float dist(Pose p1, ScenePoint p2) {return dist(p1.position, p2);}
float dist(ScenePoint p1, Pose p2) {return dist(p1, p2.position);}
