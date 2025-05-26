import pygame
from constants_for_game import clock, FPS, screen, background
from game_logic import print_basic_stats_of_character
from game_states import handle_show_ability, handle_running, handle_game_over
from game_setup import initialize_game

## TODO: need to write on terminal the rounds
if __name__ == "__main__":
    # Initialize the game
    player, opponent, player_group, current_turn, game_state, round = initialize_game()
    print_basic_stats_of_character(player_group)

    run = True
    while run:
        clock.tick(FPS)
        screen.blit(background, (0, 0))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        if game_state == "show_ability":
            game_state = handle_show_ability(player, opponent)
        elif game_state == "running":
            current_turn = handle_running(player, opponent, player_group, current_turn, events)
            if current_turn is False:
                game_state = "game_over"
        elif game_state == "game_over":
            winner="Player" if player.alive else "Opponent"
            print(f"{winner} won!")
            run = handle_game_over(winner)

        pygame.display.update()
    pygame.quit()