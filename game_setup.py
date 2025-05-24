import random
from character import Character
from constants_for_game import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

def initialize_game():
    character1 = Character(0, SCREEN_HEIGHT // 2)
    character2 = Character(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2)

    player = random.choice([character1, character2])
    opponent = character1 if player == character2 else character2

    player_group = pygame.sprite.Group()
    player_group.add(player)
    player_group.add(opponent)

    current_turn = random.choice(["player", "opponent"])

    game_state = "show_ability"

    return player, opponent, player_group, current_turn, game_state