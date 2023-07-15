import math

import pygame

from data_types.gamestate import GameState

move_speed = 200

wait_for_f3_release = False
wait_for_f4_release = False
def move_player(game_state: GameState):
    global wait_for_f3_release, wait_for_f4_release
    game_state.pressed = pygame.key.get_pressed()

    # The main loop in the root handles the fetching of key presses, so we don't need to do it here
    # To optimize, we first check if any keys we care about are pressed, and only then do we do the math
    if any([game_state.pressed[pygame.K_w], game_state.pressed[pygame.K_s], game_state.pressed[pygame.K_a],
            game_state.pressed[pygame.K_d]]):
        # Create an empty vector, then add to it based on which keys are pressed
        move = pygame.Vector2(0, 0)
        if game_state.pressed[pygame.K_w]:
            move.y -= move_speed * (game_state.dt / 1000)
        if game_state.pressed[pygame.K_s]:
            move.y += move_speed * (game_state.dt / 1000)
        if game_state.pressed[pygame.K_a]:
            move.x -= move_speed * (game_state.dt / 1000)
        if game_state.pressed[pygame.K_d]:
            move.x += move_speed * (game_state.dt / 1000)
        if move.x != 0 and move.y != 0:
            move *= 1 / math.sqrt(2)
        game_state.player_pos += move
    # When the f3 key is unpressed, toggle the debug menu
    if not game_state.pressed[pygame.K_F3] and wait_for_f3_release:
        wait_for_f3_release = False
    if game_state.pressed[pygame.K_F3] and not wait_for_f3_release:
        wait_for_f3_release = True
        game_state.show_debug = not game_state.show_debug
    # Do the same but for f4 and advanced debug
    if not game_state.pressed[pygame.K_F4] and wait_for_f4_release:
        wait_for_f4_release = False
    if game_state.pressed[pygame.K_F4] and not wait_for_f4_release:
        wait_for_f4_release = True
        game_state.debug_info.advanced_debug = not game_state.debug_info.advanced_debug