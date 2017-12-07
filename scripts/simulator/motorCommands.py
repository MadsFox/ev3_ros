
float[] motorCommand(float x1, float y1, float d1, float x2, float y2, float d2, float wheelDiameter, float wheelBase){
  float[] motorCommands = new float[2];
  float diffD= d2-d1;
  float diffX= x2-x1;
  float diffY= y2-y1;
  if(diffD == atan(diffY/diffX) && tan(diffD)/diffY == diffX && tan(diffD)*diffX == diffY){
    
  }
  return motorCommands;
}