#pragma once
#include <string>
#include <vector>
#include <algorithm>
#include "Pose.cpp"

using namespace std;

class SceneObject{
  public:
    string topic;
    virtual bool hasInside(ScenePoint sp); // to be overridden (when relevant)
    virtual bool hasInside(Pose p);
    friend void drawAllSceneObjects();
    friend int indexOf(SceneObject so);
    friend void addSceneObject(SceneObject &so);
    bool operator==(const SceneObject &so);
    string getType();
//  private:
};

vector<SceneObject*> allSceneObjects;

bool SceneObject::hasInside(ScenePoint sp) {return false;}
bool SceneObject::hasInside(Pose p) {return hasInside(p.position);}

void drawAllSceneObjects() {
 //for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i] instanceof RestrictedArea)allSceneObjects[i].draw();
 //for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i] instanceof Grid)allSceneObjects[i].draw();
 //for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i] instanceof ReferencePoint)allSceneObjects[i].draw();
 //for(int i=0;i<allSceneObjects.size();i++) allSceneObjects[i].draw();
}

int indexOf(SceneObject so) {
  vector<SceneObject*>::iterator it;
  it = std::find(allSceneObjects.begin(), allSceneObjects.end(), &so);
  if(it != allSceneObjects.end()){return std::distance(allSceneObjects.begin(), it);}
  return -1;
}

void addSceneObject(SceneObject &so) {
  allSceneObjects.push_back(&so);
  /*SceneObject old[] = allSceneObjects;
  allSceneObjects = new SceneObject[old.size()+1];
  for(int i=0;i<old.size();i++)allSceneObjects[i]=old[i];
  allSceneObjects[old.size()]=so;*/
}

bool SceneObject::operator==(const SceneObject &so){
  if(topic == so.topic){
    return 1;
  }
  return 0;
}

string SceneObject::getType(){
  return "SceneObject";
}
