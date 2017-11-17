#include <string>
#include <vector>
#include "ScenePoint.cpp"

using vector;

using namespace std;

class SceneObject {
  public:
    string topic;
    virtual bool hasInside(ScenePoint sp); // to be overridden (when relevant)
    virtual bool hasInside(Pose p);
    friend void drawAllSceneObjects();
    friend
    friend
};

bool SceneObject::hasInside(ScenePoint sp) {return false;}
bool SceneObject::hasInside(Pose p) {return hasInside(p.position);}

void drawAllSceneObjects() {
 for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i] instanceof RestrictedArea)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i] instanceof Grid)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i] instanceof ReferencePoint)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.size();i++) if(allSceneObjects[i] instanceof Robot)allSceneObjects[i].draw();}

int indexOf(SceneObject so) {
  for(int i=0;i<allSceneObjects.size();i++){if(allSceneObjects[i]==so){return i;}}
  return -1;
}

void addSceneObject(SceneObject so) {
  allSceneObjects.push_back(so);
  /*SceneObject old[] = allSceneObjects;
  allSceneObjects = new SceneObject[old.size()+1];
  for(int i=0;i<old.size();i++)allSceneObjects[i]=old[i];
  allSceneObjects[old.size()]=so;*/
}

vector<SceneObject> allSceneObjects;
