#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include "ros/ros.h"
#include "ev3_ros/MotorCommands.h"

using ev3_ros::MotorCommands;
using namespace std;

int main(int argc, char **argv) {
    int counter;
    char str[256];
    //vector for all the data in the csv file.
    vector< vector<string> > fileData;
map<string, ros::Publisher> robotPub;

    //ask in terminal for CSV file 
    cout << "Enter URI of motorCommand .csv file: ";
    cin.get(str, 256);
    string fileName(str);

    //checks if file is CSV file
    if (fileName.substr(fileName.find_last_of(".") + 1) != "csv") {
        cout << "not a csv file" << endl;
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
            counter++;
        }
        fileData.push_back(record);
       
    }
    cout << counter << " commands in file" << endl;
    
    //initiate the ROS node
    ros::init(argc, argv, "motor_command_pub_from_csv_file");

    //new nodehandler to send commands
    ros::NodeHandle n;
    
    for(vector< vector<string> >::iterator it = fileData.begin(); it != fileData.end(); ++it){
        //cout << it->at(0).c_str() << endl;
        string startTime = it->at(0).c_str(); 
        string name = it->at(1).c_str();
        if(startTime.compare("startTime") == 0){
            cout << "header line" << endl;
        }else if (name.compare("name") != 0){
            if(robotPub.find(name) != robotPub.end()){
                cout << name << " is already known" << endl;
            }else{
                cout << "new robot by the name: " << name << endl;
                
                robotPub.insert(pair<string, ros::Publisher>(name, n.advertise<MotorCommands>(name, 1000)));
            
            }
        }
    }
    
    return 0;

    
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
