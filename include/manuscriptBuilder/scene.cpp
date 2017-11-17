class Scene {
  public:
    float sw;
    float hsw;
    float sd;
  
    Scene(float sceneWidth, float sceneDepth){
      sw = sceneWidth;
      hsw = sceneWidth/2;
      sd = sceneDepth;
    }
};
