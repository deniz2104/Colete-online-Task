import pygame
from game_logic import print_ability_of_character, show_message, show_ability_status
from constants_for_game import screen, font
import time

def handle_show_ability(player, opponent):
    print_ability_of_character(
        screen,
        f"Ability chosen for player: {player.special_ability}",
        f"Ability chosen for opp: {opponent.special_ability}",
        font,
    )
    return "running"

def handle_running(player, opponent, player_group, current_turn, events):
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

    if keys[pygame.K_r]:
        player.activate_ability()

    if not opponent.ability_active and not opponent.ability_cooldown:
        opponent.activate_ability()

    player.update_ability()
    opponent.update_ability()

    for player_of_group in player_group:
        if player_of_group == player:
            player_of_group.move(moving_left, moving_right)
            player_of_group.draw(is_opponent=False)
        else:
            player_of_group.move_as_opponent(player)
            player_of_group.draw(is_opponent=True)

    if current_turn == "player":
        message = "Player Turn! Press Space to attack"
        show_message(screen, message, font)
        show_ability_status(screen, player, font)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.alive:
                    if opponent.alive and abs(player.rect.x - opponent.rect.x) < 10:
                        player.attack(opponent)
                        if not opponent.alive:
                            message = "Player Wins!"
                            show_message(screen, message, font)
                            pygame.time.delay(500)
                            return False  # End game
                        else:
                            pygame.time.delay(1000)
                            return "opponent"
    else:
        message = "Opponent Turn!"
        show_message(screen, message, font)
        show_ability_status(screen, opponent, font)
        if player.alive and abs(player.rect.x - opponent.rect.x) < 10:
            opponent.attack(player)
            if not player.alive:
                message = "Opponent Wins!"
                show_message(screen, message, font)
                pygame.time.delay(500)
                return False
            else:
                pygame.time.delay(1000)
                return "player"
    return current_turn