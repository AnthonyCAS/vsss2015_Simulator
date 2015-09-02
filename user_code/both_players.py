#!/usr/bin/python

import pygame
import socket
import struct
import time
import sys
from pygame.locals import *

from portero import *

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)

CONTROL_SERVER = ('', 9009)


pygame.init()
screen = pygame.display.set_mode((100, 100))

prev_time = time.time() * 1000 # milliseconds

LIN_VEL = 50
ANG_VEL = 3

vsss_serializer = VsssSerializer()

done = False
while not done:
    for event in pygame.event.get():
        # any other key event input
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

    red_move = Move(0.001, 0.001)
    if pygame.key.get_pressed()[K_UP]:
        red_move.linvel = LIN_VEL
    if pygame.key.get_pressed()[K_DOWN]:
        red_move.linvel = -LIN_VEL
    if pygame.key.get_pressed()[K_RIGHT]:
        red_move.angvel = -ANG_VEL
    if pygame.key.get_pressed()[K_LEFT]:
        red_move.angvel = ANG_VEL

    blue_move = Move(0.001, 0.001)
    if pygame.key.get_pressed()[K_w]:
        blue_move.linvel = LIN_VEL
    if pygame.key.get_pressed()[K_s]:
        blue_move.linvel = -LIN_VEL
    if pygame.key.get_pressed()[K_d]:
        blue_move.angvel = -ANG_VEL
    if pygame.key.get_pressed()[K_a]:
        blue_move.angvel = ANG_VEL

    out_red = VsssOutData(team=0)
    out_red.moves.append(Move())
    out_red.moves.append(red_move)

    out_blue = VsssOutData(team=1)
    out_blue.moves.append(Move())
    out_blue.moves.append(blue_move)

    out_red = vsss_serializer.dump(out_red)
    out_blue = vsss_serializer.dump(out_blue)

    cur_time = time.time() * 1000 # milliseconds
    if cur_time - prev_time > 100:
        prev_time = cur_time
        sock.sendto(out_red, CONTROL_SERVER)
        sock.sendto(out_blue, CONTROL_SERVER)
