#include "SceneObject.cpp"
#include "Pose.cpp"
#include "ScreenPoint.cpp"

class Robot : public SceneObject{
  public:
    Robot(String n)
    Robot(String n, Pose p)
    Robot(String n, ScenePoint p, float d)
  
  
  //TODO: write method to run motorcommands(mayby this is where ROS publishes)
    void run()   
  //  void moveTo(Pose p) {pose=p;}
  
    boolean hasInside(ScenePoint sp) 
      
    boolean overlappingOther() 
    
    boolean runaway() 
    
    void publishWarningFrame() 
  
    void publishWarningOnEdges() 
};
// easy constructors
Robot robot(String n) 
Robot robot(String n, Pose p) 
Robot robot(String n, ScenePoint p, float d) 
}
