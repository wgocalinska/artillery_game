import math as m
import pygame
from random import randint


def position(time, initial_velocity, initial_angle, gravity_acceleration=9.81):
    """

    :time: float, in seconds
    :initial_velocity: float, in meters over seconds
    :initial_angle: int, in degrees
    :gravity_acceleration: float, in meters over squared of second
    :return: tuple of floats, x and y coordinates
    """
    x = initial_velocity * m.cos(m.radians(initial_angle)) * time
    y = - m.pow(time, 2) * gravity_acceleration / 2 + initial_velocity * m.sin(m.radians(initial_angle)) * time
    return x, y

def finding_total_time(initial_velocity, initial_angle, gravity_acceleration=9.81):
    """
    :initial_velocity: float, in meters over seconds
    :initial_angle: int, in degrees
    :gravity_acceleration: float, in meters over squared of second
    :return: float, means total time
    """
    return initial_velocity * m.sin(m.radians(initial_angle)) * 2 / gravity_acceleration

def calculating_final_x(initial_velocity, initial_angle, total_time):
    """
    :initial_velocity: float in meters over seconds
    :initial_angle: int in degrees
    :total_time: float in seconds
    :return: float in meters
    """
    return initial_velocity * m.cos(m.radians(initial_angle)) * total_time

def if_hit(final_x, wanted_x, range=50):
    """
    :final_x: float in m
    :wanted_x: int in m
    :range: range of explosion after hit, rounded to meters
    :return: bool, true or false
    """
    if abs(wanted_x - final_x) <= range:
        return True
    else:
        return False

def getting_enemy_position_x(range=(100, 800)):
    """
    :range: tuple of ints, defines range in which enemy will be spotted
    :return: int, x_position of the enemy
    """
    return randint(range[0], range[1])

def animation(initial_angle, initial_velocity, enemy_x, resolution=(1000, 600), fps=60):
    total_time = finding_total_time(initial_velocity, initial_angle)
    final_x = calculating_final_x(initial_velocity, initial_angle, total_time)
    won = if_hit(final_x, enemy_x, range=10)
    pygame.init()
    gameDisplay = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Artillery game')
    black = (0, 0, 0)
    white = (255, 255, 255)
    clock = pygame.time.Clock()

    for time_point in range(0, int(total_time * fps + 1)):
        x, y = position(time_point / fps, initial_velocity, initial_angle)
        pygame.draw.rect(gameDisplay, (255, 0, 0), pygame.Rect(enemy_x, 500, 10, 10))
        pygame.draw.rect(gameDisplay, black, pygame.Rect(x, 500 - y, 20, 20))
        print(x, y)
        clock.tick(fps)
        pygame.display.update()
        gameDisplay.fill(white)
    pygame.quit()
    return won

def game(fps=60):
    black, white, red = (0, 0, 0), (255, 255, 255), (255, 0, 0)
    pygame.init()
    pygame.font.init()
    fonty = pygame.font.SysFont('Arial.ttf', 32)
    gameDisplay = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Artillery game")
    clock = pygame.time.Clock()
    Score = 0
    velocity = 45
    angle = 45
    enemy_x = getting_enemy_position_x()
    while True:
        rect1 = pygame.Rect(0, 0, 800, 100)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                quit()
            if event.type is pygame.KEYDOWN:
                if event.key == pygame.K_UP and velocity < 90:
                    velocity += 1
                if event.key == pygame.K_DOWN and velocity > 0:
                    velocity -= 1
                if event.key == pygame.K_LEFT and angle > 0:
                    angle -= 1
                if event.key == pygame.K_RIGHT and angle < 90:
                    angle += 1
                if event.key == pygame.K_r:
                    angle = 45
                    velocity = 45
                if event.key == pygame.K_SPACE:
                    total_time = finding_total_time(velocity, angle)
                    initial_velocity = velocity
                    initial_angle = angle
                    if if_hit(calculating_final_x(velocity, angle, total_time), enemy_x):
                        Score += 1000
                    else:
                        Score -= 100
                    for time_point in range(0, int(total_time * fps + 1)):
                        x, y = position(time_point / fps, initial_velocity, initial_angle)
                        pygame.draw.rect(gameDisplay, (255, 0, 0), pygame.Rect(enemy_x, 500, 10, 10))
                        pygame.draw.rect(gameDisplay, black, pygame.Rect(x, 500 - y, 20, 20))
                        clock.tick(fps)
                        pygame.display.update()
                        gameDisplay.fill(white)
                    enemy_x = getting_enemy_position_x()
            temp = "Velocity = {0}[m/s], Angle = {1}[deg], Score = {2}[points], Enemy is {3} m away".format(velocity, angle, Score, enemy_x)
            values_text = fonty.render(temp, False, (0, 0, 0))
            velues_rect = values_text.get_rect(center=rect1.center)
            gameDisplay.blit(values_text, velues_rect)
            pygame.draw.rect(gameDisplay, (255, 0, 0), pygame.Rect(enemy_x, 500, 10, 10))
            pygame.draw.rect(gameDisplay, black, pygame.Rect(0, 500, 20, 20))
            pygame.display.flip()
            gameDisplay.fill(white)
game()
