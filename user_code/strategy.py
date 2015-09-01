#!/usr/bin/python

import socket
import struct
import numpy as np
import time

VISION_SERVER = ('', 9009)
CONTROL_SERVER = ('', 9009)
SERVER = ('', 9091)

prev_time = time.time() * 1000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SERVER)

sock.sendto('', VISION_SERVER)

class PID:
    def __init__(self, kp, kd, ki=0):
        self.Kp = kp
        self.Kd = kd
        self.Ki = ki
        self.prev_error = 0

    def update(self, error):
        P = self.Kp * error
        D = self.Kd * (error - self.prev_error)
        self.prev_error = error
        return P + D

class Position:
    def __init__(self, x, y, theta=0):
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self):
        return 'x: %s, y: %s, theta: %s' % (self.x, self.y, self.theta)

    def vector_to(self, position):
        return np.array([position.x, position.y]) - np.array([self.x, self.y])

    def distance_to(self, position):
        v = self.vector_to(position)
        return np.linalg.norm(v)

    def angle_to(self, position, deg=True):
        v = self.vector_to(position)
        ang = np.arctan2(v[1], v[0])
        if deg:
            return ang*180/np.pi
        else:
            return ang

class Move:
    def __init__(self, linvel=0, angvel=0):
        self.linvel = linvel
        self.angvel = angvel

    def __str__(self):
        return '<MOVE> Lin: %s, Ang: %s' % (self.linvel, self.angvel)


lin_pid = PID(10, 10, 0)
ang_pid = PID(0.2, 0.2, 0)


def normalize_angle(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def go_to_from(goal, start):
    linerr = start.distance_to(goal)
    linvel = min(50, lin_pid.update(linerr))
    if linerr < 0.1:
        linvel = 0
        angerr = normalize_angle(goal.theta - start.theta)
    else:
        angerr = normalize_angle(start.angle_to(goal) - start.theta)
    angvel = min(8, max(-8, ang_pid.update(angerr)))
    print('ERROR:', linerr, angerr)
    return Move(linvel, angvel)


class VsssInData:
    def __init__(self, team, ball):
        self.team = team
        self.ball = ball


class VsssOutData:
    def __init__(self, moves=None, team=0):
        if moves is None:
            self.moves = []
        else:
            self.moves = moves
        self.team = team


robots_per_team = 2
my_team = 0


class VsssSerializer:
    def load(self, data):
        data = struct.unpack('%sf' % (len(data)/4), data)
        team = []
        for i in range(2):
            team.append(Position(data[3*robots_per_team*my_team + i*3],
                                 data[3*robots_per_team*my_team + i*3+1],
                                 data[3*robots_per_team*my_team + i*3+2]))
        ball = Position(data[2*3*robots_per_team],
                        data[2*3*robots_per_team + 1])
        return VsssInData(team, ball)

    def dump(self, out_data):
        data = [float(out_data.team)]
        for move in out_data.moves:
            data.append(move.linvel)
            data.append(move.angvel)
        return struct.pack('%sf' % len(data), *data)



vsss_serializer = VsssSerializer()


if __name__ == '__main__':
    while True:
        in_data, addr = sock.recvfrom(1024)
        cur_time = time.time() * 1000 # milliseconds
        if cur_time - prev_time > 50:
            prev_time = cur_time
            in_data = vsss_serializer.load(in_data)

            out_data = VsssOutData()
            move = go_to_from(Position(-68, 0, 90), in_data.team[0])
            print(move)
            print(in_data.team[0])
            out_data.moves.append(move)
            out_data.moves.append(Move())

            out_data = vsss_serializer.dump(out_data)
            sock.sendto(out_data, CONTROL_SERVER)
