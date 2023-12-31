import pygame.mouse
from pygame import Vector2

from data_types.gamestate import GameState


def get_torch_polygon(game_state: GameState) -> list[Vector2]:
    mouse_pos = pygame.mouse.get_pos()
    between_vec = pygame.Vector2(mouse_pos[0] - game_state.player_pos.x, mouse_pos[1] - game_state.player_pos.y)
    between_vec.scale_to_length(game_state.config.view_distance)
    # Rotate vector by 30 degrees
    between_vec.rotate_ip(game_state.config.view_angle)

    # Add player position to get final rotated vector position
    rotated_vector_top = Vector2(game_state.player_pos.x + between_vec.x,
                                 game_state.player_pos.y + between_vec.y)
    between_vec.rotate_ip(game_state.config.view_angle * -2)

    # Add player position to get final rotated vector position
    rotated_vector_bottom = Vector2(game_state.player_pos.x + between_vec.x,
                                    game_state.player_pos.y + between_vec.y)
    return [rotated_vector_top, rotated_vector_bottom, game_state.player_pos]


def trace_to_mouse(game_state: GameState):
    if not game_state.debug_info.advanced_debug:
        pygame.draw.polygon(game_state.screen, "white", get_torch_polygon(game_state),
                            0)