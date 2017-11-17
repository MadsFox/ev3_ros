class Scene {
  public:
    Scene(float sceneWidth, float sceneDepth);
    Scene(const Scene &_scene);
    Scene(){};
    ~Scene();
//  private:
    float sw;
    float hsw;
    float sd;

};

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
