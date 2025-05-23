import pygame
import random
import time
from constants_for_game import *
from character import Character 
from Button import Button

## activez abilitatea asta cand vreau si o am pentru 3 secunde
## calculatorul in schimb o activeaza random si o foloseste tot pentru 3 secunde 
## am timp de regenerare pentru abilitate de 5 secunde
## trebuie sa fac handling la bara de viata, ele acum se suprapun

def print_basic_stats_of_character(group):
    counter=1
    for character in group: 
        print("Character",counter,":power =",character.attack_power,", defense =",character.defense_power)
        counter+=1

def print_ability_of_character(screen,player_message,opponent_message,font,duration=3):
    start=time.time()
    while time.time()-start < duration:
        screen.blit(background,(0,0))
        text_surface=font.render(player_message,True,(255,255,255))
        text_surface_opponent=font.render(opponent_message,True,(255,255,255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9))
        text_rect_opponent = text_surface_opponent.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.2))
        screen.blit(text_surface_opponent,text_rect_opponent)
        screen.blit(text_surface,text_rect)
        pygame.display.update()

def show_message(screen, message, font):
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(text_surface, text_rect)
    pygame.display.update()


if __name__ == "__main__":
    run = True
    ability_chosen = False
    character1 = Character(0, SCREEN_HEIGHT // 1.5)
    character2 = Character(SCREEN_WIDTH, SCREEN_HEIGHT // 1.5)
    player = random.choice([character1, character2])
    opponent = character1 if player == character2 else character2
    player_group = pygame.sprite.Group()
    player_group.add(player)
    player_group.add(opponent)
    print_basic_stats_of_character(player_group)
    game_state = "show_ability"
    current_turn= random.choice(["player","opponent"])

    while run:
        clock.tick(FPS)
        screen.blit(background, (0, 0))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if game_state == "show_ability":
            print_ability_of_character(screen, "Ability chosen for player: " + str(player.special_ability),"Ability chosen for opp: " + str(opponent.special_ability),font)
            game_state = "running"
        elif game_state == "running":
            keys = pygame.key.get_pressed()
            moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

            for player_of_group in player_group:
                if player_of_group == player:
                    player_of_group.move(moving_left, moving_right)
                else:
                    player_of_group.move_as_opponent(player)
                player_of_group.draw()
            if current_turn == "player":
                message = "Player Turn! Press Space to attack"
                show_message(screen, message, font)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player.alive:
                            if opponent.alive:  # Check if the opponent is alive
                                player.attack(opponent)
                                if not opponent.alive:  # Check if the opponent died
                                    message = "Player Wins!"
                                    show_message(screen, message, font)
                                    pygame.time.delay(500)
                                    run = False
                                else:
                                    current_turn = "opponent"
                                    pygame.time.delay(500)
            else:
                message = "Opponent Turn!"
                show_message(screen, message, font)
                if player.alive and abs(player.rect.x-opponent.rect.x) <20:  ##aici trebuie sa verific daca playerul e langa el
                    opponent.attack(player)
                    if not player.alive:  # Check if the player died
                        message = "Opponent Wins!"
                        show_message(screen, message, font)
                        pygame.time.delay(500)
                        run = False  
                    else:
                        current_turn = "player"
                        pygame.time.delay(500)
        pygame.display.update()
    pygame.quit()