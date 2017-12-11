#!/usr/bin/env python

from sceneObjects import *

epsilon = 0.01  # 1 cm


class Route:  # find bedre navn
    no_of_steps = 0
    poses = []  # no assumptions here about speed
    travelDist = 0  # in metres will only be approximate

    def __init__(self, n, pp, td):
        self.no_of_steps = n
        self.poses = pp
        self.travelDist = td

    # Route(from, to):
    #    Route r=None
    #    r= forwardRoute(from,to)
    #    if(r==None){
    #      println("Route("+from+", "+to+") too complicated try something else!!!!!!!!!!!!!!!!")
    #      System.exit(1)
    #      noOfSteps=0 poses=None noOfSteps=0}
    #    else{noOfSteps=r.noOfSteps poses=r.poses}
    # }


def forward_route(from_pose, to):
    travel_dist = 0
    first_half = []
    last_half = []

    # catch infinite loops:
    path_length = 1

    current_from = from_pose
    current_to = to
    while dist(current_from, current_to) >= 2 * epsilon and path_length < 100000:
        path_length += 2
        station1 = None
        best_dist = 10000000
        for k in range(0, 101):  # use odd number (100+1) so "straight ahead" is also an option
            suggest = current_from.klone()
            suggest.move_rel_phi_d(-maxTurn + float(k) / 101 * 2 * maxTurn, epsilon)
            suggest_dist = dist(suggest, current_to)
            if suggest_dist < best_dist:
                best_dist = suggest_dist
                station1 = suggest

        first_half.append(station1)
        travel_dist += epsilon
        current_from = station1
        last_half.append(current_to)

        station_n = None
        best_dist = 10000000
        for k in range(0, 101):  # use odd number (100+1) so "straight ahead" is also an option
            suggest = current_to.klone()
            suggest.move_rel_phi_d(-maxTurn + float(k) / 101 * 2 * maxTurn,
                                   -epsilon)  # break symmetry by change of direction
            suggest_dist = dist(suggest, current_from)
            if suggest_dist < best_dist:
                best_dist = suggest_dist
                station_n = suggest

        current_to = station_n
        travel_dist += epsilon

    all_poses = []
    for i in first_half:
        all_poses[i] = first_half[i]
    all_poses[len(first_half)] = current_from.avg(current_to)
    travel_dist = dist(from_pose, to)
    for i in last_half:
        all_poses[len(first_half) + len(last_half) - i] = last_half[i]

    if path_length >= 100000:
        print("Route(" + from_pose + ", " + to + ") too complicated try something else")
        sys.exit(1)
    return Route(len(all_poses), all_poses, travel_dist)
    # / TEST AND MAKE A WARNING IF travelDist >> robotTurningDiameter*PI + dist(from,to)


# #############################end
# #############################


def backward_route(from_pose, to):
    r = mk_backward_route_from_both_ends_internal(from_pose, to)
    if r is None:
        print("Route(" + from_pose + ", " + to + ") too complicated try something else")
        sys.exit(1)
    return r


def mk_backward_route_from_both_ends_internal(from_pose, to):
    r = forward_route(to, from_pose)
    if r is None:
        return None
    # reverse
    moves = r.no_of_steps / 2
    if r.no_of_steps / 2 * 2 == r.no_of_steps:
        moves += 1
    for i in moves:
        current_pose = r.poses[i]
        r.poses[i] = r.poses[r.no_of_steps - i - 2]
        r.poses[r.no_of_steps - i - 1] = current_pose
    r.poses[r.no_of_steps - 1] = to
    return r


def forward_turn_left_route(from_pose, radius, angle):
    center = from_pose.position.klone()
    center.move_rel_x_rel_y(-cos(radians(from_pose.direction)) * radius, sin(radians(from_pose.direction)) * radius)
    phi0 = normalize_angle(from_pose.direction + 90)
    travel_length = radius * radians(angle)
    no_of_steps = round(travel_length / epsilon)
    poses = [no_of_steps]
    for i in no_of_steps:
        phi = normalize_angle(phi0 - (i + 1) * angle / no_of_steps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalize_angle(phi - 90))

    return Route(no_of_steps, poses, travel_length)


def forward_turn_right_route(from_pose, radius, angle):
    center = from_pose.position.klone()
    center.move_rel_x_rel_y(cos(radians(from_pose.direction)) * radius, -sin(radians(from_pose.direction)) * radius)
    phi0 = normalize_angle(from_pose.direction - 90)
    travel_length = radius * radians(angle)
    no_of_steps = round(travel_length / epsilon)
    poses = [no_of_steps]
    for i in no_of_steps:
        phi = normalize_angle(phi0 + (i + 1) * angle / no_of_steps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalize_angle(phi + 90))

    return Route(no_of_steps, poses, travel_length)


def backward_turn_left_route(from_pose, radius, angle):
    center = from_pose.position.klone()
    center.move_rel_x_rel_y(-cos(radians(from_pose.direction)) * radius, sin(radians(from_pose.direction)) * radius)
    phi0 = normalize_angle(from_pose.direction + 90)
    travel_length = radius * radians(angle)
    no_of_steps = round(travel_length / epsilon)
    poses = [no_of_steps]
    for i in no_of_steps:
        phi = normalize_angle(phi0 + (i + 1) * angle / no_of_steps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalize_angle(phi - 90))

    return Route(no_of_steps, poses, travel_length)


def backward_turn_right_route(from_pose, radius, angle):
    center = from_pose.position.klone()
    center.move_rel_x_rel_y(cos(radians(from_pose.direction)) * radius, -sin(radians(from_pose.direction)) * radius)
    phi0 = normalize_angle(from_pose.direction - 90)
    travel_length = radius * radians(angle)
    no_of_steps = round(travel_length / epsilon)
    poses = [no_of_steps]
    for i in no_of_steps:
        phi = normalize_angle(phi0 - (i + 1) * angle / no_of_steps)
        poses[i] = Pose(center.x + sin(radians(phi)) * radius, center.y + cos(radians(phi)) * radius,
                        normalize_angle(phi + 90))

    return Route(no_of_steps, poses, travel_length)
