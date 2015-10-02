from user_code.settings import *

def reset_red_team(red_team):
    for robot, pos, ori in zip(red_team, red_team_positions, red_team_orientations):
        robot.setLinearVelocity([0, 0, 0])
        # This eliminates any momentum, [0, 0, 0] doesn't work
        robot.setAngularVelocity([0.01] * 3)
        robot.worldPosition = pos + [3.5]
        robot.alignAxisToVect(ori, 1, 1)
    

def reset_blue_team(blue_team):
    for robot, pos, ori in zip(blue_team, blue_team_positions, blue_team_orientations):
        robot.setLinearVelocity([0, 0, 0])
        # This eliminates any momentum, [0, 0, 0] doesn't work
        robot.setAngularVelocity([0.01] * 3)
        robot.worldPosition = pos + [3.5]
        robot.alignAxisToVect(ori, 1, 1)


def reset_ball(ball):
    ball.setLinearVelocity([0, 0, 0])
    # This eliminates any momentum, [0, 0, 0] doesn't work
    ball.setAngularVelocity([0.01] * 3)
    ball.worldPosition = ball_position + [2.2]
