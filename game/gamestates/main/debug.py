import math

import psutil

import pygame
from pygame.font import Font

from data_types.gamestate import GameState
from game.gamestates.main.debug_rtx import draw_to_map_nodes
from utils.convert_size import convert_size

debug_text = "0 FPS"
fps_counter = 0
move_frame_counter = 0
distance_travelled = 0
font: Font
Y = 16

current_proc = psutil.Process()


def preload(game_state: GameState):
    global font
    font = pygame.font.Font('assets/fonts/firacode.ttf', 16)


def update(game_state: GameState):
    global debug_text, fps_counter, move_frame_counter, distance_travelled
    if game_state.debug_info.advanced_debug:
        draw_to_map_nodes(game_state)
    fps_counter += 1
    move_frame_counter += 1
    if game_state.show_debug:
        if move_frame_counter >= 100:
            distance_travelled_x = game_state.debug_info.last_pos[0] - game_state.player_pos.x
            distance_travelled_y = game_state.debug_info.last_pos[1] - game_state.player_pos.y
            distance_travelled = math.sqrt(distance_travelled_x ** 2 + distance_travelled_y ** 2)
            move_frame_counter = 0
            game_state.debug_info.last_pos = [game_state.player_pos.x, game_state.player_pos.y]
        if fps_counter >= 10:
            debug_text = (f"{round(game_state.clock.get_fps())} FPS "
                          # How much time it takes to actually compute the frame
                          f"| {round(game_state.debug_info.frame_time * 1e-6, 2):.2} frame ms "
                          # How long we sleep for to get the desired framerate. Higher is better
                          f"| {round(game_state.debug_info.sleep_time * 1e-6, 2):.2} sleep ms "
                          f"| {round(distance_travelled)} px/100 frames "
                          f"| {convert_size(current_proc.memory_info().rss)} RAM")
            fps_counter = 0
        x_offset = pygame.font.Font.size(font, debug_text)
        text = font.render(debug_text, True, (0, 255, 0), None)
        text_rect = text.get_rect()
        text_rect.center = ((x_offset[0] // 2), Y // 2)
        game_state.screen.blit(text, text_rect)