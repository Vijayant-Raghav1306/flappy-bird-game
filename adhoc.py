import sys
import pygame
import random

gravity = 3
bir_movement = 0
pygame.init()

screen = pygame.display.set_mode((576, 1024))
background = pygame.image.load("background-day.png").convert()
background = pygame.transfrom.scale2x(background)

bird  = pygame.imaqe.load("bluebird-midflap.png").convert()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
    screen.blit(background,(0, 0))
    pygame.display.update()
    screen.blit(background, (0, 0))

    bird_movement += gravity

    screen.blit(bird, (100, bird_movement))
    pygame.display.update() 