#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "ros/ros.h"
#include "ev3_ros/MotorCommands.h"

using ev3_ros::MotorCommands;
using namespace std;

int main(int argc, char **argv) {
    char str[256];
    //vector for all the data in the csv file.
    vector< vector<string> > fileData;

    //ask in terminal for CSV file 
    cout << "Enter URI of motorCommand .csv file: ";
    cin.get(str, 256);
    string fileName(str);

    //checks if file is CSV file
    if (fileName.substr(fileName.find_last_of(".") + 1) != "csv") {
        cout << "not a csv file";
        return 0;
    }

    ifstream infile(str);


    while (infile) {
        string s;
        if(!getline(infile, s)) break;
        
        istringstream ss(s);
        vector<string> record;
        
        while(ss){
            string s;
            if(!getline(ss,s,',')) break;
            record.push_back(s);
            cout << s;
        }
        fileData.push_back(record);
        cout << endl;
    }
    return 0;

    //initiate the ROS node
    ros::init(argc, argv, "motor_command_pub_test_node");

    //new nodehandler to send commands
    ros::NodeHandle n;

    ros::Publisher motor_command_pub = n.advertise<MotorCommands>("motor_command", 1000);

    ros::Rate loop_rate(10);

    int duration = 0;

    MotorCommands mc;

    /*while (ros::ok())
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
    }*/

    return 0;
}
