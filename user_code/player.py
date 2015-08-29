#!/usr/bin/python

import pygame
import socket
import struct
import time
import sys
from pygame.locals import *

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


sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)

server_address = ('', 9009)


pygame.init()
screen = pygame.display.set_mode((100, 100))

prev_time = time.time() * 1000 # milliseconds

LIN_VEL = 50
ANG_VEL = 3

done = False
while not done:
    for event in pygame.event.get():
        # any other key event input
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

    team_message = [0.001] * 5
    team_message[0] = float(sys.argv[1])

    if pygame.key.get_pressed()[K_UP]:
        team_message[1] = LIN_VEL
    if pygame.key.get_pressed()[K_DOWN]:
        team_message[1] = -LIN_VEL
    if pygame.key.get_pressed()[K_RIGHT]:
        team_message[2] = -ANG_VEL
    if pygame.key.get_pressed()[K_LEFT]:
        team_message[2] = ANG_VEL

    if pygame.key.get_pressed()[K_w]:
        team_message[3] = LIN_VEL
    if pygame.key.get_pressed()[K_s]:
        team_message[3] = -LIN_VEL
    if pygame.key.get_pressed()[K_d]:
        team_message[4] = -ANG_VEL
    if pygame.key.get_pressed()[K_a]:
        team_message[4] = ANG_VEL

    cur_time = time.time() * 1000 # milliseconds
    if cur_time - prev_time > 100:
        prev_time = cur_time
        team = struct.pack('%sf' % len(team_message),*team_message)
        sent = sock.sendto(team, server_address)
