import pygame
pygame.init()
pygame.display.set_caption("Duel Battle")
clock = pygame.time.Clock()
SCREEN_WIDTH=800
SCREEN_HEIGHT=int(SCREEN_WIDTH*0.85)
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS=60
background=pygame.image.load('background.png').convert()
left_margin=-20
right_margin=SCREEN_HEIGHT+20
font = pygame.font.SysFont("arialblack", 28)
