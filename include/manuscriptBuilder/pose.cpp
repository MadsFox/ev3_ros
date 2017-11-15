using "screenPoint.h"

class Pose {// for a robot
  ScenePoint position; 
  float direction; // 0..360;
  Pose(float xx, float yy, float dd) {position = new ScenePoint(xx,yy); direction=dd;}
  Pose(ScenePoint ss, float dd) {position = ss; direction=dd;}
  
  Pose klone() {return new Pose(position.klone(),direction);} // intuitively same as clone, but returns object of right class
  @ Override
  String toString() {return position+"*phi="+direction;}

  void moveRelPhiD(float deltaPhi, float deltaDist) {
    // phi added to current direction, but scaled by deltaDist AND SOME CONSTANT THAT DEPENDS ON PHYSICAL DETAILS OF THE ROBOT
    moveAbsPhiD(direction+deltaPhi*abs(deltaDist)*4,deltaDist);
  }

  void moveAbsPhiD(float phi, float deltaDist) {
    // set new direction and move
    direction=normalizeAngle(phi);
    position.moveRelPhiD(direction,deltaDist);
  }
}

// easy constructor:
Pose pose(float x, float y, float d) {return new Pose(x,y,d);}

Pose avg(Pose p1, Pose p2) {
  return new Pose(avg(p1.position,p2.position),(p1.direction+p2.direction)/2);
}

// directions internally in degrees; memotech. as n,e,s,w etc.
// south means looking out of from scene towards audience

float north=0;
float east=90;
float south=180;
float west=270;
float northEast=north+90/2;
float southEast=south-90/2;
float northWest=west+90/2;
float southWest=west-90/2;
float nne=north+90/4;
float ene=east-90/4;
float ese=east+90/4;
float sse=south-90/4;
float ssw=south+90/4;
float wsw=west-90/4;
float wnw=west+90/4;
float nnw=360-90/4;

float normalizeAngle(float phi) {if(phi<0)return normalizeAngle(phi+360);else if(phi>=360)return normalizeAngle(phi-360); else return phi;}
float normalizeAngleRad(float phi) {if(phi<0)return normalizeAngle(phi+TWO_PI);else if(phi>=TWO_PI)return normalizeAngle(phi-TWO_PI); else return phi;}

static final float robotTurningDiameter = 0.7;
  // Currently only used for checking feasibility of generated route
  // in mkXXXXXRouteXXXX; should be correlated with constant epsilon and expected robot diameter

float dist(Pose p1, Pose p2) {
  // plain euclidian, ignoring direction
  return dist(p1.position, p2.position);
}
float dist(Pose p1, ScenePoint p2) {return dist(p1.position, p2);}
float dist(ScenePoint p1, Pose p2) {return dist(p1, p2.position);}
