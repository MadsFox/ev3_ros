#include <math.h>
#include "screenPoint.cpp"
#include "scene.cpp"

class ScenePoint {
  public:
    float x;
    float y;
    ScenePoint(float xx,float yy){x=xx;y=yy;}
  
    ScenePoint klone() {return new ScenePoint(x,y);}
    
    ScreenPoint toScreenPoint() {
      int scrX=round(width/2+x/sceneWidth*width);
      int scrY=round(height-y/sceneDepth*height);
      return new ScreenPoint(scrX,scrY);}
  
    String toString() {return "<"+x+","+y+">";}
  
    boolean runaway(){return x>hsw||x<-hsw||y>sd||y<0;}
  
    void moveRelXRelY(float deltaX, float deltaY) {x+=deltaX;y+=deltaY;}
  
    void moveRelPhiD(float phi, float deltaDist) {
      float sinNewDir=sin(radians(phi)); float cosNewDir=cos(radians(phi));
      moveRelXRelY(sinNewDir*deltaDist, cosNewDir*deltaDist);   
    }
};

// easy constructor
ScenePoint p(float x, float y) {return new ScenePoint(x,y);}

ScenePoint avg(ScenePoint p1, ScenePoint p2) {return new ScenePoint((p1.x+p2.x)/2,(p1.y+p2.y)/2);}

float toScreenUnit(float sceneDist, Scene s) {return sceneDist/s.sw*width;}

float dist(ScenePoint p1, ScenePoint p2) {
  return sqrt( sq(p1.x-p2.x) + sq(p1.y-p2.y));
}
