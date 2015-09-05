def reset_red_team(red_team):
    red_team_positions = [
        [10, -10, 3.5],
        [10, 10, 3.5],
	[10, 0, 3.5],
    ]

    for robot, pos in zip(red_team, red_team_positions):
        robot.setLinearVelocity([0, 0, 0])
        # This eliminates any momentum, [0, 0, 0] doesn't work
        robot.setAngularVelocity([0.01] * 3)
        robot.worldPosition = pos
        robot.alignAxisToVect([-1, 0, 0], 1, 1)
    

def reset_blue_team(blue_team):
    blue_team_positions = [
        [-10, 10, 3.5],
        [-10, -10, 3.5],
	[-10, 0, 3.5],
    ]

    for robot, pos in zip(blue_team, blue_team_positions):
        robot.setLinearVelocity([0, 0, 0])
        # This eliminates any momentum, [0, 0, 0] doesn't work
        robot.setAngularVelocity([0.01] * 3)
        robot.worldPosition = pos
        robot.alignAxisToVect([1, 0, 0], 1, 1)


def reset_ball(ball):
    ball.setLinearVelocity([0, 0, 0])
    # This eliminates any momentum, [0, 0, 0] doesn't work
    ball.setAngularVelocity([0.01] * 3)
    ball.worldPosition = [0, 0, 2.2]
