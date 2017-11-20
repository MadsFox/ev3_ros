class Scene {
  public:
    bool operator==(Scene s);
    Scene(float sceneWidth, float sceneDepth);
    Scene(const Scene &_scene);
    Scene(){};
    ~Scene();
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
