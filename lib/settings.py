# RT_CMD and BT_CMD are how you command your team
# RT stands for red team and BT stands for blue team
# CMD stands for command
# There are two options:
#     CMD_TYPE_VEL: You must provide linear and angular velocities
#     CMD_TYPE_POW: You must provide left and right motor powers

CMD_TYPE_VEL = 'velocidad'
CMD_TYPE_POW = 'potencia'

RT_CMD = CMD_TYPE_VEL
BT_CMD = CMD_TYPE_VEL

# Set the number of players
RT = 3
BT = 3

red_team_positions = [
    [10, -10],
    [10, 10],
    [10, 0],
]

blue_team_positions = [
    [-10, 10],
    [-10, -10],
    [-10, 0],
]

ball_position = [0, 0]

SERVER = ('0.0.0.0', 9001)