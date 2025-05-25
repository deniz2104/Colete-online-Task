import pygame
import time
from constants_for_game import screen, font, background, SCREEN_WIDTH, SCREEN_HEIGHT

def print_basic_stats_of_character(group):
    counter = 1
    for character in group:
        print(f"Character {counter}: power = {character.attack_power}, defense = {character.defense_power}")
        counter += 1

def print_ability_of_character(screen, player_message, opponent_message, font, duration=3):
    start = time.time()
    while time.time() - start < duration:
        screen.blit(background, (0, 0))
        text_surface = font.render(player_message, True, (0, 0, 0))
        text_surface_opponent = font.render(opponent_message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9))
        text_rect_opponent = text_surface_opponent.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.2))
        screen.blit(text_surface_opponent, text_rect_opponent)
        screen.blit(text_surface, text_rect)
        pygame.display.update()

def show_message(screen, message, font, height=50):
    text_surface = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, height))
    screen.blit(text_surface, text_rect)

def show_ability_status(screen, character, font):
    if character.ability_active:
        message = f"Ability Active: {character.special_ability}"
    elif character.ability_cooldown:
        message = "Character is on cooldown"
    else:
        message = "Character can use ability"
    show_message(screen, message,font , height=100)
    pygame.display.update()