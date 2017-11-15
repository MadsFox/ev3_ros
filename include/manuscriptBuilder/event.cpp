#include "robot.h"
#include "pose.h"

// keep track of all events prescribed by manuscript and make it possible for "draw" to execute it;
// haha, den skal da bruge absolut tid !!!!

import java.util.*;

class Event implements Comparable {
  float time; // seconds from beginning of story
  Robot rob;
  Pose nextPose;  // in nextPose=null, this means a no-event; used for implementing waiting
  
  Event(float tt,Robot rr,Pose pp) {time=tt;rob=rr;nextPose=pp.klone();eventList.add(this);}

  Event(float tt,Robot rr, float waitingTime) {time=tt+waitingTime;rob=rr;nextPose=null;eventList.add(this);}
  
  @Override
  public int compareTo(Object e) {
    float d= time - ((Event)e).time;
    if(d<0) return -1; if(d>0) return 1; return 0;
  }
  
  @Override
  String toString() {return time+": "+rob.name+nextPose;}

}

ArrayList<Event> eventList = new ArrayList<Event>();

float timeOfLastGeneratedEvent() {
  float t=-1;
  for(int i=0;i<eventList.size();i++)
    if(eventList.get(i).time>t) t=eventList.get(i).time;
  return t;
}

float timeOfLastGeneratedEvent(Robot r) {
  float t=-1;
  for(int i=0;i<eventList.size();i++)
    if(eventList.get(i).rob==r && eventList.get(i).time>t) t=eventList.get(i).time;
  return t;
}
void sortEventList() {Collections.sort(eventList);}

void printEventList() {for(int i=0;i<eventList.size();i++) println(eventList.get(i)+"");}

int initialMachineTime;

float simulationTime;

void initTime() {initialMachineTime = millis();}

float currentSimulationTime() {return ((float)(millis()-initialMachineTime))/1000;}

void executeCurrentEvents() {
  float t= currentSimulationTime();
 // println("executeCurrentEvents() at sim. time "+t+", remaining events: " +eventList.size());
  while(eventList.size()>0 && eventList.get(0).time<t) {
    if(eventList.get(0).nextPose!=null) eventList.get(0).rob.pose=eventList.get(0).nextPose;
    eventList.remove(0);}
}

boolean noMoreEvents() {return eventList.isEmpty();}
  
