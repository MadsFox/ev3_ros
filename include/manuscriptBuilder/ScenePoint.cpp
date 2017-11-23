#pragma once
#include <math.h>
#include <string>
#include <sstream>
#define _USE_MATH_DEFINES
//#include "screenPoint.cpp"
#include "Scene.cpp"

using namespace std;

class ScenePoint{
  public:
    //Class methods
    //ScenePoint klone();
    string toString();
    string getType();
    bool runaway();
    void moveRelXRelY(float deltaX, float deltaY);
    void moveRelPhiD(float phi, float deltaDist);
    float dist(ScenePoint p);
    bool operator==(ScenePoint sp);
    friend ScenePoint p(Scene scene, float x, float y);//friend functions can accessed class members outside of object/class.
    friend ScenePoint avg(Scene scene, ScenePoint p1, ScenePoint p2);
    friend float dist(ScenePoint p1, ScenePoint p2);
    //Constructors
    ScenePoint(Scene _scene, float _x,float _y);
    ScenePoint(const ScenePoint &_sp);
    ScenePoint(){};
    ~ScenePoint();
//  private:
    float x;
    float y;
    Scene scene;
    /* Do not need to convert from sceen to screen when working with robot.
    ScreenPoint toScreenPoint() {
      int scrX=round(width/2+x/sceneWidth*width);
      int scrY=round(height-y/sceneDepth*height);
      return new ScreenPoint(scrX,scrY);}
    */
};

//defining constructor
ScenePoint::ScenePoint(Scene _scene, float _x,float _y){
  scene = _scene;
  x=_x;
  y=_y;
}

ScenePoint::ScenePoint(const ScenePoint &_sp){
  scene = _sp.scene;
  x = _sp.x;
  y = _sp.y;  
}
//defining methods
//Trying with a copy constructor instead
//ScenePoint ScenePoint::klone() {return new ScenePoint(scene,x,y);}

ScenePoint::~ScenePoint(){
  delete this;
}

string ScenePoint::toString() {
  ostringstream stm;
  stm << "<" << x << "," << y << "," << scene.sw << "," << scene.sd << ">";
  return stm.str();
}

string ScenePoint::getType(){
  return "ScenePoint";
}

bool ScenePoint::runaway(){return x>scene.hsw||x<-scene.hsw||y>scene.sd||y<0;}

void ScenePoint::moveRelXRelY(float deltaX, float deltaY) {x+=deltaX;y+=deltaY;}

void ScenePoint::moveRelPhiD(float phi, float deltaDist) {
  float sinNewDir=sin(2*M_PI*phi/360); float cosNewDir=cos(2*M_PI*phi/360);
  moveRelXRelY(sinNewDir*deltaDist, cosNewDir*deltaDist);   
}

float ScenePoint::dist(ScenePoint p) {
  return sqrt( sqrt(x-p.x) + sqrt(y-p.y));
}

bool ScenePoint::operator==(ScenePoint sp){
  if(x == sp.x && y == sp.y && scene == sp.scene){
    return true;
  }
  return false;
}

// easy constructor
ScenePoint scenePoint(Scene _scene, float x, float y) {return ScenePoint(_scene,x,y);}

ScenePoint avg(Scene _scene, ScenePoint p1, ScenePoint p2) {return ScenePoint(_scene,(p1.x+p2.x)/2,(p1.y+p2.y)/2);}

//float toScreenUnit(float sceneDist, Scene s) {return sceneDist/s::sw*width;}

float dist(ScenePoint p1, ScenePoint p2) {
  return sqrt( sqrt(p1.x-p2.x) + sqrt(p1.y-p2.y));
}
