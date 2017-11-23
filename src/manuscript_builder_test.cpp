//#include "../include/manuscriptBuilder/Scene.cpp"
//#include "../include/manuscriptBuilder/ScenePoint.cpp"
//#include "../include/manuscriptBuilder/Pose.cpp"
//#include "../include/manuscriptBuilder/SceneObject.cpp"
//#include "../include/manuscriptBuilder/Robot.cpp"
//#include "../include/manuscriptBuilder/Event.cpp"
//#include "../include/manuscriptBuilder/Route.cpp"
#include "../include/manuscriptBuilder/ManuscriptHelpers.cpp"
#include <iostream>

using namespace std;
using namespace manuscript_helpers;

int main(int argc, char **argv)
{
  cout << "first executable file written from buttom up" << endl;
  initScene(500, 500);
  cout << "i succeced in running manuscript builder code(initScene)" << endl;         
  
  initialPose("ev3_1", 250.0f, 250.0f, 20.0f);
  cout << "i succeced in running manuscript builder code(initalPose)" << endl;         
  
  return 0;
}
