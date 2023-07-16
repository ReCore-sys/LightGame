import time

import pygame

from data_types.gamestate import GameState
import game.gamestates.main.debug as debug
from game.gamestates.main.map import draw_map
from game.gamestates.main.movement import move_player
from game.gamestates.main.torch import trace_to_mouse


def accurate_delay(delay):
    """ Function to provide accurate time delay in millisecond
    """
    _ = time.perf_counter() + delay / 1000
    while time.perf_counter() < _:
        pass


X = 60
Y = 16


player_pos: pygame.Vector2
debug_text = "0 FPS"
fps_counter = 0


def preload(game_state: GameState):
    game_state.player_pos = pygame.Vector2(game_state.screen.get_width() / 2, game_state.screen.get_height() / 2)
    game_state.debug_info.last_pos = [game_state.player_pos.x, game_state.player_pos.y]
    game_state.screen.fill("black")
    return game_state


def update(game_state: GameState):
    global debug_text
    frame_start = time.time_ns()

    move_player(game_state)
    trace_to_mouse(game_state)
    if game_state.show_debug:
        debug.update(game_state)

    # Increase the stored tick
    # If we need to rerender the screen
    pygame.draw.circle(game_state.screen, "red", game_state.player_pos, 10)
    draw_map(game_state)
    pygame.display.update()
    # Now a bunch of post render stuff
    game_state.screen.fill("black")

    # Check if we have closed the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.close = True

    sleep_start = time.time_ns()
    game_state.dt = game_state.clock.tick(game_state.config.framerate)
    # elapsed = (time.time_ns() - frame_start)
    # if elapsed < (1 / game_state.config.framerate) * 1e9:
    #     accurate_delay((1 / game_state.config.framerate) * 1000 - elapsed / 1e6)
    #     # time.sleep(((1 / framerate) * 1e9 - elapsed) / 1e9)
    sleep_end = time.time_ns()
    game_state.debug_info.sleep_time = sleep_end - sleep_start
    game_state.debug_info.frame_time = time.time_ns() - frame_start
    return game_state