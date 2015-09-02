#!/usr/bin/python

import socket
import struct
import sys
import numpy as np
import time

VISION_SERVER = ('', 9009)
CONTROL_SERVER = ('', 9009)
# SERVER = ('', 9091)

prev_time = time.time() * 1000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(SERVER)

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
    def __init__(self, linvel=99999, angvel=99999):
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
    def __init__(self, red_team, blue_team, ball):
        self.red_team = red_team
        self.blue_team = blue_team
        self.ball = ball


class VsssOutData:
    def __init__(self, moves=None, team=0):
        if moves is None:
            self.moves = []
        else:
            self.moves = moves
        self.team = team


robots_per_team = 2

class VsssSerializer:
    def load(self, data):
        data = struct.unpack('%sf' % (len(data)/4), data)
        red_team = []
        blue_team = []
        my_team = 0
        for i in range(2):
            red_team.append(Position(data[3*robots_per_team*my_team + i*3],
                                 data[3*robots_per_team*my_team + i*3+1],
                                 data[3*robots_per_team*my_team + i*3+2]))
        my_team = 1
        for i in range(2):
            blue_team.append(Position(data[3*robots_per_team*my_team + i*3],
                                 data[3*robots_per_team*my_team + i*3+1],
                                 data[3*robots_per_team*my_team + i*3+2]))
        ball = Position(data[2*3*robots_per_team],
                        data[2*3*robots_per_team + 1])
        return VsssInData(red_team, blue_team, ball)

    def dump(self, out_data):
        data = [float(out_data.team)]
        for move in out_data.moves:
            data.append(move.linvel)
            data.append(move.angvel)
        return struct.pack('%sf' % len(data), *data)



vsss_serializer = VsssSerializer()


if __name__ == '__main__':
    def help():
        return """Ejecute el script de cualquiera de las 2 formas, una para cada equipo:
        ./player 0
        ./player 1"""

    # Help the user if he doesn't know how to use the command
    if len(sys.argv) != 2:
        print help()
        sys.exit()
    elif sys.argv[1] != '0' and sys.argv[1] != '1':
        print help()
        sys.exit()



    while True:
        in_data, addr = sock.recvfrom(1024)
        cur_time = time.time() * 1000 # milliseconds
        if cur_time - prev_time > 50:
            prev_time = cur_time
            in_data = vsss_serializer.load(in_data)

            if sys.argv[1] == '0':
                my_team = in_data.red_team
            else:
                my_team = in_data.blue_team

            out_data = VsssOutData(team=int(sys.argv[1]))
            dest = in_data.ball
            dest.theta = 90

            dest.y = min(20, max(-20, dest.y))
            if sys.argv[1] == '0':
                dest.x = 68
            else:
                dest.x = -68
            move = go_to_from(dest, my_team[0])

            out_data.moves.append(move)
            out_data.moves.append(Move())

            out_data = vsss_serializer.dump(out_data)
            sock.sendto(out_data, CONTROL_SERVER)
