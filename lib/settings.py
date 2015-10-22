# Set the number of players
RT = 3
BT = 3

red_team_positions = [
    [10, -10],
    [10, 10],
    [10, 0],
]

red_team_orientations = [
    [-1, 0, 0],
    [-1, 0, 0],
    [-1, 0, 0]
]

blue_team_positions = [
    [-10, 10],
    [-10, -10],
    [-10, 0],
]

blue_team_orientations = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0]
]

ball_position = [0, 0]

THIS_SERVER = ('0.0.0.0', 9001)
STRATEGY_SERVERS = [('0.0.0.0', 9002)]

VISION_LATENCY = 50             # milliseconds
VISION_ACCURACY = 1
VISION_ANGLE_ACCURACY = 1