// scene coordinate system
//    x-axis front edge of scene shown in bottom of screen window
//     and with zero in the middle
//    y-axis points into the scene; zero at front edge of scene

// internal units are meters





class ScreenPoint {
  int x;
  int y;
  ScreenPoint(int xx,int yy){
    x=xx;y=yy;
  }
}

float toScreenUnit(float sceneDist, Scene s) {return sceneDist/s.sw*width;}

float dist(ScenePoint p1, ScenePoint p2) {
  return sqrt( sq(p1.x-p2.x) + sq(p1.y-p2.y));
}


