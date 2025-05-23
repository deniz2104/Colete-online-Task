import pygame
import random
import time
from constants_for_game import *
from character import Character 
from Button import Button

##fiecare dintre ei poate avea o abilitate speciala

def print_basic_stats_of_character(group):
    counter=1
    for character in group: 
        print("Character",counter,":power =",character.attack_power,", defense =",character.defense_power)
        counter+=1

def print_ability_of_character(screen,message,font,duration=2):
    start=time.time()
    while time.time()-start < duration:
        screen.blit(background,(0,0))
        text_surface=font.render(message,True,(255,255,255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
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
    print_basic_stats_of_character(player_group)
    heal_ability_button = Button("Heal", 0, 200, 200, 300)
    attack_ability_button = Button("Attack", 300, 200, 200, 300)
    half_damage_ability_button = Button("Half Damage", 600, 200, 200, 300)
    game_state = "choose_ability"

    while run:
        clock.tick(FPS)
        screen.blit(background, (0, 0))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()


        if game_state == "choose_ability":
            heal_ability_button.is_clicked(mouse_pos)
            half_damage_ability_button.is_clicked(mouse_pos)
            attack_ability_button.is_clicked(mouse_pos)

            heal_ability_button.draw()
            half_damage_ability_button.draw()
            attack_ability_button.draw()

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and not ability_chosen:
                    if heal_ability_button.top_rect.collidepoint(mouse_pos):
                        if player.special_ability != "self_heal":
                            player.special_ability = None
                        ability_chosen = True
                    elif half_damage_ability_button.top_rect.collidepoint(mouse_pos):
                        if player.special_ability != "half_damage_ability":
                            player.special_ability = None
                        ability_chosen = True
                    elif attack_ability_button.top_rect.collidepoint(mouse_pos):
                        if player.special_ability != "extra_attack":
                            player.special_ability = None
                        ability_chosen = True
            if ability_chosen:
                print_ability_of_character(screen, "Ability chosen: " + str(player.special_ability), font)
                game_state = "running"
        elif game_state == "running":
            keys = pygame.key.get_pressed()
            moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

            for player_of_group in player_group:
                if player_of_group.alive:
                    player_of_group.move(moving_left, moving_right)
                    player_of_group.draw()

        pygame.display.update()
    pygame.quit()