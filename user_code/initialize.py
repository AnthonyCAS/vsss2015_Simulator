def reset_red_team(red_team):
    red_team_positions = [
        [0, 10, 3.5],
        [10, 10, 3.5],
        [-10, 10, 3.5]
    ]

    for robot, pos in zip(red_team, red_team_positions):
        robot.worldPosition = pos
    

def reset_blue_team(blue_team):
    blue_team_positions = [
        [0, -10, 3.5],
        [10, -10, 3.5],
        [-10, -10, 3.5]
    ]

    for robot, pos in zip(blue_team, blue_team_positions):
        robot.worldPosition = pos


def reset_ball(ball):
    ball.worldPosition = [0, 0, 2.2]
