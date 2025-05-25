import pygame
import time
from game_logic import print_ability_of_character, show_message, show_ability_status
from constants_for_game import screen, font,background

def handle_show_ability(player, opponent):
    print_ability_of_character(
        screen,
        f"Ability chosen for player: {player.special_ability}",
        f"Ability chosen for opp: {opponent.special_ability}",
        font,
    )
    return "running"

def handle_game_over(winner):
    start_time = time.time()
    while time.time() - start_time < 3:
        screen.blit(background, (0, 0))
        message = f"{winner} Wins!"
        show_message(screen, message, font)
        pygame.display.update()
    return False

def handle_running(player, opponent, player_group, current_turn, events):
    handle_abilities(player, opponent)

    handle_movement(player, opponent, player_group)

    current_turn = handle_turn(player, opponent, current_turn, events)

    return current_turn


def handle_abilities(player, opponent):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        player.activate_ability()

    if not opponent.ability_active and not opponent.ability_cooldown:
        opponent.activate_ability()

    player.update_ability()
    opponent.update_ability()


def handle_movement(player, opponent, player_group):
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

    for character in player_group:
        if character == player:
            character.move(moving_left, moving_right)
            character.draw(is_opponent=False)
        else:
            character.move_as_opponent(player)
            character.draw(is_opponent=True)


def handle_turn(player, opponent, current_turn, events):
    if current_turn == "player":
        return handle_player_turn(player, opponent, events)
    else:
        return handle_opponent_turn(player, opponent)


def handle_player_turn(player, opponent, events):
    message = "Player Turn! Press Space to attack"
    show_message(screen, message, font)
    show_ability_status(screen, player, font)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.alive:
                if opponent.alive and abs(player.rect.x - opponent.rect.x) < 10:
                    player.attack(opponent)
                    if not opponent.alive:
                        return handle_game_over("Player")
                    else:
                        pygame.time.delay(500)
                        return "opponent"
    return "player"


def handle_opponent_turn(player, opponent):
    message = "Opponent Turn!"
    show_message(screen, message, font)
    show_ability_status(screen, opponent, font)

    if player.alive and abs(player.rect.x - opponent.rect.x) < 10:
        opponent.attack(player)
        if not player.alive:
            return handle_game_over("Opponent")
        else:
            pygame.time.delay(500)
            return "player"
    return "opponent"