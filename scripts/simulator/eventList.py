// keep track of all events prescribed by manuscript and make it possible for "draw" to execute it; //<>//
// haha, den skal da bruge absolut tid !!!!

import java.util.*;

class Event implements Comparable {
  float time; // seconds from beginning of story
  Robot rob;
  Pose nextPose;  // in nextPose=null, this means a no-event; used for implementing waiting

  Event(float tt, Robot rr, Pose pp) {
    time=tt;
    rob=rr;
    nextPose=pp.klone();
    eventList.add(this);
  }

  Event(float tt, Robot rr, float waitingTime) {
    time=tt+waitingTime;
    rob=rr;
    nextPose=null;
    eventList.add(this);
  }

  @Override
    public int compareTo(Object e) {
    float d= time - ((Event)e).time;
    if (d<0) return -1; 
    if (d>0) return 1; 
    return 0;
  }

  @Override
    String toString() {
    return time+": "+rob.name+nextPose;
  }
}

ArrayList<Event> eventList = new ArrayList<Event>();

float timeOfLastGeneratedEvent() {
  float t=-1;
  for (int i=0; i<eventList.size(); i++)
    if (eventList.get(i).time>t) t=eventList.get(i).time;
  return t;
}

float timeOfLastGeneratedEvent(Robot r) {
  float t=-1;
  for (int i=0; i<eventList.size(); i++)
    if (eventList.get(i).rob==r && eventList.get(i).time>t) t=eventList.get(i).time;
  return t;
}
void sortEventList() {
  Collections.sort(eventList);
}

void printEventList() {
  for (int i=0; i<eventList.size(); i++) {
    println(eventList.get(i)+"");
  }
}

void writeEventListToFile(String fileName) {
  ArrayList<String> RobotEvents = new ArrayList<String>();
  RobotEvents.add("\"time\",\"name\",\"x\",\"y\",\"direction\",\"nextX\",\"nextY\",\"nextDirection\"");
  for (int i=0; i<eventList.size(); i++) { 
    if (eventList.get(i).nextPose!=null && eventList.get(i ).rob.pose!=null) {
      RobotEvents.add(
        "\""+ eventList.get(i).time+
        "\",\""+eventList.get(i).rob.name+
        "\",\""+eventList.get(i).rob.pose.position.x+
        "\",\""+eventList.get(i).rob.pose.position.y+
        "\",\""+eventList.get(i).rob.pose.direction+
        "\",\""+eventList.get(i).nextPose.position.x+
        "\",\""+eventList.get(i).nextPose.position.y+
        "\",\""+eventList.get(i).nextPose.direction+"\""
        );
    } else if (eventList.get(i).rob.pose!=null) {
      RobotEvents.add(
        "\""+ eventList.get(i).time+
        "\",\""+eventList.get(i).rob.name+
        "\",\""+eventList.get(i).rob.pose.position.x+
        "\",\""+eventList.get(i).rob.pose.position.y+
        "\",\""+eventList.get(i).rob.pose.direction + "\",\" - no nextPose value\""
        );
    } else if (eventList.get(i).nextPose!=null) {
      RobotEvents.add(
        "\""+ eventList.get(i).time+
        "\",\""+eventList.get(i).rob.name+
        "\",\" - no pose.x value"+
        "\",\" - no pose.y value"+
        "\",\" - no pose.direction value"+
        "\",\""+eventList.get(i).nextPose.position.x+
        "\",\""+eventList.get(i).nextPose.position.y+
        "\",\""+eventList.get(i).nextPose.direction+"\""
        );
    } else {
      RobotEvents.add(
        "\""+ eventList.get(i).time+
        "\",\""+eventList.get(i).rob.name+"\",\" - no avalible pose values\",\"\",\"\",\"\",\"\",\"\""
        );
    }
  }
  String[] fileData = RobotEvents.toArray(new String[0]);
  saveStrings(fileName, fileData);
}

void printMotorEventList() {
  Event lastEvent = eventList.get(0);
  for (int i=0; i<eventList.size(); i++) { 
    if (eventList.get(i)==lastEvent) {
      println("the same"
        //TODO: write method calls to get motor commands
        );
    } else if (eventList.get(i).rob.pose.direction==eventList.get(i).nextPose.direction) {
      println("motor diff: 0");
    } else if (eventList.get(i).rob.pose.direction!=eventList.get(i).nextPose.direction) {
      float x1 = eventList.get(i).rob.pose.position.x;
      float y1 =eventList.get(i).rob.pose.position.y;
      float direction1 = eventList.get(i).rob.pose.direction;
      float x2 = eventList.get(i).nextPose.position.x;
      float y2 = eventList.get(i).nextPose.position.y;
      float direction2 = eventList.get(i).nextPose.direction;    
      println("motor diff: ");
    }
    lastEvent = eventList.get(i);
  }
}

void writeMotorEventListToFile(String fileName) {
  ArrayList<String> MotorCommands = new ArrayList<String>();
  for (int i=0; i<eventList.size(); i++) { 
    if (eventList.get(i).nextPose!=null) {
      MotorCommands.add(""
        //TODO: write method calls to get motor commands
        );
    } else {
      MotorCommands.add(""
        );
    }
  }
  String[] fileData = MotorCommands.toArray(new String[0]);
  saveStrings(fileName, fileData);
}

int initialMachineTime;

float simulationTime;

void initTime() {
  initialMachineTime = millis();
}

float currentSimulationTime() {
  return ((float)(millis()-initialMachineTime))/1000;
}

void executeCurrentEvents() {
  float t= currentSimulationTime();
  //println("executeCurrentEvents() at sim. time "+t+", remaining events: " +eventList.size() + ", " + eventList.get(0).rob.toString());
  while (eventList.size()>0 && eventList.get(0).time<t) {
    if (eventList.get(0).nextPose!=null) eventList.get(0).rob.pose=eventList.get(0).nextPose;
    eventList.remove(0);
  }
}

boolean noMoreEvents() {
  return eventList.isEmpty();
}