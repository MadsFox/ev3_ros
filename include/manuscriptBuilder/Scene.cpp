#pragma once
#include <string>

using namespace std;

class Scene {
  public:
    bool operator==(Scene s);
    void operator=(Scene* s);
    string getType();
    Scene(float sceneWidth, float sceneDepth);
    Scene(const Scene &_scene);
    Scene(){};
    ~Scene();
    Scene scene(float sceneWidth, float sceneDepth);
    Scene scene(const Scene &_scene);
//  private:
    float sw;
    float hsw;
    float sd;

};

bool Scene::operator==(Scene s){
  if(sw == s.sw && hsw == s.hsw && sd == s.sd){
    return true;
  }
  return false;
}

void Scene::operator=(Scene* s){
  sw = s->sw;
  hsw == s->hsw;
  sd == s->sd;
}

Scene::Scene(float sceneWidth, float sceneDepth){
  sw = sceneWidth;
  hsw = sceneWidth/2;
  sd = sceneDepth;
}

Scene::Scene(const Scene &_scene){
  sw = _scene.sw;
  hsw = _scene.hsw;
  sd = _scene.sd;  
}

Scene::~Scene(){
  delete this;
}

Scene Scene::scene(float sceneWidth, float sceneDepth) {return Scene(sceneWidth, sceneDepth);}
Scene Scene::scene(const Scene &_scene) {return Scene(_scene);}

string Scene::getType(){
  return "Scene";
}
