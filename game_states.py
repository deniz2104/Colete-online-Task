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
    # Static variables to track the round number and last printed turn
    if not hasattr(handle_running, "round_number"):
        handle_running.round_number = 1
        handle_running.last_turn = None

    # Print the round number only when the turn changes
    if handle_running.last_turn != current_turn:
        if current_turn == "player":
            print(f"Round {handle_running.round_number}:")
        handle_running.last_turn = current_turn

    # Handle abilities, movement, and turns
    handle_abilities(player, opponent)
    handle_movement(player, opponent, player_group)
    current_turn = handle_turn(player, opponent, current_turn, events)

    # Increment the round number after the player's turn
    if current_turn == "player" and handle_running.last_turn == "opponent":
        handle_running.round_number += 1

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

def display_ability_status(character, current_turn="player",ability_used=False):
    message="Character 1 " if current_turn == "player" else "Character 2 "
    if character.ability_active:
        print(f"{message}activates ability:{character.special_ability}")
        ability_used = True
    elif not ability_used:
        print("No ability activated")

def handle_player_turn(player, opponent, events):
    message = "Player Turn! Press Space to attack"
    show_message(screen, message, font)
    show_ability_status(screen, player, font)
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.alive:
                print("Character 1 attacks")
                if opponent.alive and abs(player.rect.x - opponent.rect.x) < 10:
                    player.attack(opponent)
                    print(f"Character 2 has {opponent.health} health")
                    pygame.time.delay(500)
                    return "opponent"
                elif not opponent.alive:
                    return handle_game_over("Player")
    return "player"


def handle_opponent_turn(player, opponent):
    message = "Opponent Turn!"
    show_message(screen, message, font)
    show_ability_status(screen, opponent, font)

    if player.alive and abs(player.rect.x - opponent.rect.x) < 10:
        print("Character 2 attacks")
        opponent.attack(player)
        print(f"Character 1 has {player.health} health")
        pygame.time.delay(500)
        return "player"
    elif not player.alive:
        return handle_game_over("Opponent")
    return "opponent"