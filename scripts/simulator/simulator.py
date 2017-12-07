float sceneWidth = 10; //meters
float sceneDepth = 5; //meters

String scriptFileName = "hubahop";

void setup() {
  // the following should preserve the proportions of (sceneWidth,sceneDepth);
  size(2000,1000);
  frameRate(24);
  background(51);
  manuscript();
  sortEventList(); // IMPORTANT!!!!
  //printEventList();
  initTime();
}

void draw() {
  background(51);
  executeCurrentEvents();
  drawAllSceneObjects();
//////  saveFrame("frames/"+(frameCount<1000?"0":"")+(frameCount<100?"0":"")+(frameCount<10?"0":"")+frameCount+".png");
  if(noMoreEvents()) noLoop();
}