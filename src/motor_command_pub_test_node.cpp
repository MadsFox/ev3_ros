#include "ros/ros.h"
#include "ev3_ros/MotorCommands.h"

using ev3_ros::MotorCommands;
//using namespace ros;

int main(int argc, char **argv)
{
  ros::init(argc, argv, "motor_command_pub_test_node");

  ros::NodeHandle n;

  ros::Publisher motor_command_pub = n.advertise<MotorCommands>("motor_command", 1000);

  ros::Rate loop_rate(10);

  int duration = 0;

  MotorCommands mc;

  while (ros::ok())
  {
    switch(duration%100) {
      case 1 :
        mc.right_speed = 100;
        mc.left_speed = -50;
        break;
      case 6 :
        mc.right_speed = -50;
        mc.left_speed = 100;
        break;
    }
  
    motor_command_pub.publish(mc);

    ros::spinOnce();

    loop_rate.sleep();

    ++duration;
  }

  return 0;
}
