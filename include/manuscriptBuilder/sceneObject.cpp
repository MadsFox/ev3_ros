#include <string>
#include "scenePoint.cpp"

using namespace std;

class SceneObject {
  public:
    string topic;
    virtual bool hasInside(ScenePoint sp) {return false;} // to be overridden (when relevant)
    virtual bool hasInside(Pose p) {return hasInside(p.position);}
};

void drawAllSceneObjects() {
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof RestrictedArea)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof Grid)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof ReferencePoint)allSceneObjects[i].draw();
 for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i] instanceof Robot)allSceneObjects[i].draw();}

int indexOf(SceneObject so) {
  for(int i=0;i<allSceneObjects.length;i++) if(allSceneObjects[i]==so)return i;
  return -1;
}

void addSceneObject(SceneObject so) {
  SceneObject old[] = allSceneObjects;
  allSceneObjects = new SceneObject[old.length+1];
  for(int i=0;i<old.length;i++)allSceneObjects[i]=old[i];
  allSceneObjects[old.length]=so;
}

SceneObject allSceneObjects[0]
