#!/usr/bin/env python

from eventList import *


class MotorCommand:
    from_pose = Pose
    to_pose = Pose
    left_motor_speed = 0
    right_motor_speed = 0

    def __init__(self, from_pose, to_pose):
        self.from_pose = from_pose
        self.to_pose = to_pose
        self.calculate_speeds()
        motor_commands.append(self)

    def calculate_speeds(self):
        left_motor_speed=100
        right_motor_speed=100
        return None


motor_commands = []


def create_motor_commands():
    prev_event = None
    prev_time = 0
    for event in eventList:

        motor_commands[prev_time] = \
            {"name": event.rob.name,
             "start_time": prev_time,
             "start_x": prev_event.nextPose.x,
             "start_y": prev_event.nextPose.y,
             "start_d": prev_event.nextPose.d,
             "end_time": event.time,
             "end_x": event.nextPose.x,
             "end_y": event.nextPose.y,
             "end_d": event.nextPose.d,
             "left_motor_speed": MotorCommand.left_motor_speed,
             "right_motor_speed": MotorCommand.right_motor_speed}
        event.nextPose
        prev_event = event
        prev_time = event.time
