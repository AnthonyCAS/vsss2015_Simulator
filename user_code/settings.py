from lib.settings import *

# Set the number of players
RT = 1
BT = 1

red_team_positions = [
    # [10, -10],
    # [10, 10],
    [10, 0],
]

red_team_orientations = [
    [-1, 0, 0]
]

blue_team_positions = [
    # [-10, 10],
    # [-10, -10],
    [-10, -50],
]

blue_team_orientations = [
    [1, 0, 0]
]

ball_position = [0, 50]

SERVER = ('0.0.0.0', 9001)
