// scene coordinate system
//    x-axis front edge of scene shown in bottom of screen window
//     and with zero in the middle
//    y-axis points into the scene; zero at front edge of scene

// internal units are meters

class ScreenPoint {
  public:
    int x;
    int y;
    ScreenPoint(int xx,int yy){
      x=xx;y=yy;
    }
};
