import pygame.mouse

from data_types.gamestate import GameState

view_distance = 500
view_angle = 15


def trace_to_mouse(game_state: GameState):
    mouse_pos = pygame.mouse.get_pos()
    between_vec = pygame.Vector2(mouse_pos[0] - game_state.player_pos.x, mouse_pos[1] - game_state.player_pos.y)
    between_vec.scale_to_length(view_distance)
    # Rotate vector by 30 degrees
    between_vec.rotate_ip(view_angle)

    # Add player position to get final rotated vector position
    rotated_vector_top = (game_state.player_pos.x + between_vec.x,
                          game_state.player_pos.y + between_vec.y)
    between_vec.rotate_ip(view_angle * -2)

    # Add player position to get final rotated vector position
    rotated_vector_bottom = (game_state.player_pos.x + between_vec.x,
                             game_state.player_pos.y + between_vec.y)
    pygame.draw.polygon(game_state.screen, "white", [rotated_vector_top, rotated_vector_bottom, game_state.player_pos],
                        0)