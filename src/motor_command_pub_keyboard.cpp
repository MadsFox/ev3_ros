#include "ros/ros.h"
#include "ev3_ros/MotorCommands.h"
#include <geometry_msgs/Twist.h>

using ev3_ros::MotorCommands;

MotorCommands mc;

void turtlebotKeyCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
  //float x = 500 * msg->linear.x;
  //float z = msg->angular.z;
  mc.right_speed = msg->linear.x + msg->angular.z;
  mc.left_speed = msg->linear.x - msg->angular.z;
//  ROS_INFO("trying to print liniar x values: %f and angular z values: %f", x, z);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "motor_command_pub_keyboard");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("turtlebot_teleop/cmd_vel", 50, turtlebotKeyCallback);


  ros::Publisher motor_command_pub = n.advertise<MotorCommands>("motor_command", 50);

  ros::Rate loop_rate(10);

  int duration = 0;

  while (ros::ok())
  {
    motor_command_pub.publish(mc);

//    ROS_INFO("motor commands - speed: %i - direction: %i", mc.speed, mc.direction);

    ros::spinOnce();

    loop_rate.sleep();

    ++duration;
  }

  return 0;
}
