import pygame.draw
import shapely
from pygame import Vector2

from data_types.gamestate import GameState
from utils.vector_stuffs import within_polygon
from game.gamestates.main.torch import get_torch_polygon
from utils.vector_stuffs import int_ify_list


def find_line_nodes(game_state: GameState) -> list[Vector2]:
    torch_polygon = get_torch_polygon(game_state)
    i = 0
    while i < len(torch_polygon):
        for node in game_state.map.Nodes:
            possible_intersection = shapely.LineString([(node.start_x, node.start_y), (node.end_x, node.end_y)])

            findline = shapely.LineString([torch_polygon[0], (game_state.player_pos.x, game_state.player_pos.y)])
            if findline.intersects(possible_intersection):
                pygame.draw.circle(game_state.screen, "blue", (possible_intersection.xy[0][0], possible_intersection.xy[0][1]), 10)
                for point in game_state.map.UniquePoints:
                    if within_polygon(point.x, point.y, int_ify_list(torch_polygon)):
                        # Insert this corner into the list of points at i
                        torch_polygon.insert(i + 1, Vector2(point.x, point.y))
                        view_vector = point.rotate(point.angle_to(game_state.player_pos))
                        view_vector.scale_to_length(game_state.config.view_distance)
                        torch_polygon[i + 1] = view_vector
                        # dedupe
                        torch_polygon = [t for n, t in enumerate(torch_polygon) if t not in torch_polygon[:n]]
        i += 1
    pygame.draw.polygon(game_state.screen, "red", torch_polygon)
    return torch_polygon


def compute_polygon(game_state: GameState) -> list[Vector2]:
    find_line_nodes(game_state)