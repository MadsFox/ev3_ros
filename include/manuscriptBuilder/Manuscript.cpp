#include "ManuscriptHelpers.h"
#include "Pose.h"
#include "Robot.h"

using namespace manuscriptHelpers;
using namespace pose;
using namespace robot;
// the method manuscript initiates some data structures, but does not make anything happen

void manuscript() {
  //robot takes one argument, the name of its advertiser topic node
  Robot ev3_robot1 = robot("ev3_1");
  initialPose(ev3_robot1, pose(hsw/2+1, sd/4, west));

  wait(ev3_robot1, 2);
  
  moveTo(ev3_robot1, pose(-hsw/2,sd/2, south));

  moveTo(ev3_robot1,    pose(-hsw/4,sd*0.75, north));

  moveTo(ev3_robot1,    pose(-hsw/8,sd/4, south));

  wait(ev3_robot1, 3);
    
  synchronize();  // denne her er fiks: alle venter til sidste mand følger trop
    
  moveToBacking(ev3_robot1, pose(-hsw/8+1,sd/4+1, south)); 

  wait(ev3_robot1,0.5); 

  moveTo(ev3_robot1,    pose(+hsw/8+1.5,sd/4, south));

  synchronize();

  moveTo(ev3_robot1, pose(-1,sd/2, east));

  synchronize();
    
  moveTo(ev3_robot1,  pose(-0.25,sd/2, east));

  moveToBacking(ev3_robot1, pose(-1,sd/2-0.75, nne));

  moveTo(ev3_robot1, pose(-1,sd/2, north));

  circleRight(ev3_robot1,0.75,180);
  circleRight(ev3_robot1,0.375,180);
  circleRightBacking(ev3_robot1,0.375,40);
  circleRight(ev3_robot1,0.375,40);

  moveToBacking(ev3_robot1, pose(0,sd/2-0.75, north));

  moveTo(ev3_robot1, pose(0,sd/2-0.1, north));//north
  moveToBacking(ev3_robot1, pose(-0.5,sd/2-0.75, nne));
 
  moveTo(ev3_robot1, pose(1,sd+2, north));
}

void meetAndGreat(Robot r1, Robot r2, float x, float y) {
  moveTo(r1, x-1, y, east); 
  moveTo(r2, x+1, y, west);
  synchronize(r1,r2);
  moveTo(r1, x-0.25, y, east);
  moveTo(r2, x+0.25, y, west);
  wait(r1,1); wait(r2,1);
  moveToBacking(r1, x-1, y, east); 
  moveToBacking(r2, x+1, y, west);
  wait(r1,0.5); wait(r2,0.5);
}
