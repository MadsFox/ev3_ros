#include "Robot.cpp"
//#include "Pose.cpp"
#include <vector>
#include <time.h>
#include <string>
#include <iostream>
#include <algorithm>

// keep track of all events prescribed by manuscript and make it possible for "draw" to execute it;
// haha, den skal da bruge absolut tid !!!!

class Event {
  public: 
    Event(float tt,Robot rr,Pose pp);
    Event(float tt,Robot rr, float waitingTime);
    Event(){};
    ~Event();
    int compareTo(Event e);
    string toString();
    void addEvent(Event &e);
    float timeOfLastGeneratedEvent();
    float timeOfLastGeneratedEvent(Robot r);
    void sortEventList();
    void printEventList();
    void initTime();
    float currentSimulationTime();
    void executeCurrentEvents();
    bool noMoreEvents();
//  private:
    float time; // seconds from beginning of story
    Robot rob;
    Pose nextPose;  // in nextPose=null, this means a no-event; used for implementing waiting
    float initialMachineTime;
    float simulationTime;
    std::vector<Event*> eventList;
};

Event::Event(float tt,Robot rr,Pose pp) {time=tt;rob=rr;nextPose=pp.klone();addEvent(*this);}

Event::Event(float tt,Robot rr, float waitingTime) {
  time=tt+waitingTime;
  rob=rr;
  nextPose=rr.pose;
  addEvent(*this);
}

int Event::compareTo(Event e) {
  float d= time - ((Event)e).time;
  if(d<0) return -1; if(d>0) return 1; return 0;
}

string Event::toString() {
  ostringstream stm;
  stm << time << ": " << rob.topic << nextPose.toString();
  return stm.str();
}

void Event::addEvent(Event &e) {
  eventList.push_back(&e);
}

float Event::timeOfLastGeneratedEvent() {
  float t=-1;
  for(int i=0;i<eventList.size();i++)
    if(eventList[i]->time>t) t=eventList[i]->time;
  return t;
}

float Event::timeOfLastGeneratedEvent(Robot r) {
  float t=-1;
  for(int i=0;i<eventList.size();i++)
    if(eventList[i]->rob==r && eventList[i]->time>t) t=eventList[i]->time;
  return t;
}
void Event::sortEventList() {std::sort(eventList.begin(), eventList.end());}

void Event::printEventList() {for(int i=0;i<eventList.size();i++) cout << eventList[i] << "";}

void Event::initTime() {initialMachineTime = (float)clock()/CLOCKS_PER_SEC;}

float Event::currentSimulationTime() {return (((float)clock()/CLOCKS_PER_SEC)-initialMachineTime)/1000;}

void Event::executeCurrentEvents() {
  float t= currentSimulationTime();
 // println("executeCurrentEvents() at sim. time "+t+", remaining events: " +eventList.size());
  while(eventList.size()>0 && eventList[0]->time<t) {
    if(!(eventList[0]->nextPose==eventList[0]->rob.pose)) eventList[0]->rob.pose=eventList[0]->nextPose;
    eventList.erase(eventList.begin());}
}

bool Event::noMoreEvents() {return eventList.empty();}
