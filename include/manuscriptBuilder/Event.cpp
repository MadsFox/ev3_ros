#include "Robot.cpp"
#include "Pose.cpp"
#include <vector>
#include <time.h>

// keep track of all events prescribed by manuscript and make it possible for "draw" to execute it;
// haha, den skal da bruge absolut tid !!!!

class Event {
  float time; // seconds from beginning of story
  Robot rob;
  Pose nextPose;  // in nextPose=null, this means a no-event; used for implementing waiting
  
  Event(float tt,Robot rr,Pose pp) {time=tt;rob=rr;nextPose=pp.klone();eventList.add(this);}

  Event(float tt,Robot rr, float waitingTime) {time=tt+waitingTime;rob=rr;nextPose=null;eventList.add(this);}
  
  public int compareTo(Object e) {
    float d= time - ((Event)e).time;
    if(d<0) return -1; if(d>0) return 1; return 0;
  }
  String toString() {return time+": "+rob.name+nextPose;}

}

std::vector<Event> eventList;

float timeOfLastGeneratedEvent() {
  float t=-1;
  for(int i=0;i<eventList.size();i++)
    if(eventList[i].time>t) t=eventList[i].time;
  return t;
}

float timeOfLastGeneratedEvent(Robot r) {
  float t=-1;
  for(int i=0;i<eventList.size();i++)
    if(eventList[i].rob==r && eventList[i].time>t) t=eventList[i].time;
  return t;
}
void sortEventList() {std::sort(eventList);}

void printEventList() {for(int i=0;i<eventList.size();i++) println(eventList[i]+"");}

float initialMachineTime;

float simulationTime;

void initTime() {initialMachineTime = (float)clock()/CLOCKS_PER_SEC}

float currentSimulationTime() {return (((float)clock()/CLOCKS_PER_SEV)-initialMachineTime)/1000;}

void executeCurrentEvents() {
  float t= currentSimulationTime();
 // println("executeCurrentEvents() at sim. time "+t+", remaining events: " +eventList.size());
  while(eventList.size()>0 && eventList[0].time<t) {
    if(eventList[0].nextPose!=null) eventList[0].rob.pose=eventList[0].nextPose;
    eventList.erase(0);}
}

bool noMoreEvents() {return eventList.empty();}
  
