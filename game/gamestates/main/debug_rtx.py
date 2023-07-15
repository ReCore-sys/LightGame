import math

import pygame
from numba import jit
from numba.typed import List
from shapely import Point

from shapely.geometry import LineString

from data_types.gamestate import GameState
from game.gamestates.main.torch import get_torch_polygon


# using numba to speed up the function
@jit(nopython=True, cache=True, fastmath=True)
def within_polygon(x: int, y: int, poly: list[[int, int]], tolerance=5):
    n = len(poly)
    inside = False
    x_ints = 0.0

    # Original polygon check
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_ints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_ints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    # Check distance to edges
    if not inside:
        for i in range(n):
            p1x, p1y = poly[i]
            p2x, p2y = poly[(i + 1) % n]

            dist = abs((p2y - p1y) * x - (p2x - p1x) * y + p2x * p1y - p2y * p1x) / math.hypot(p2y - p1y, p2x - p1x)

            if dist <= tolerance:
                return True

    return inside


def draw_to_map_nodes(game_state: GameState):
    points_of_interest = List()

    torch_polygon = get_torch_polygon(game_state)
    [points_of_interest.append((x.x, x.y)) for x in game_state.map.UniquePoints]
    points_of_interest.append((torch_polygon[0][0], torch_polygon[0][1]))
    points_of_interest.append((torch_polygon[1][0], torch_polygon[1][1]))

    for point in points_of_interest:
        # draw a line from the player to the point
        pygame.draw.aaline(game_state.screen, "blue", game_state.player_pos, point, 5)
        pygame.draw.circle(game_state.screen, "blue", (int(point[0]), int(point[1])), 10)

        # Draw all the intersections of the blue lines and the map nodes
        for node in game_state.map.Nodes:
            # Using shapely to find the intersection because I am stupid and can't do it myself
            line = LineString([(game_state.player_pos.x, game_state.player_pos.y), (point[0], point[1])])
            other_line = LineString([(node.start_x, node.start_y), (node.end_x, node.end_y)])
            intercept: Point = line.intersection(other_line)
            # If there is no intersection, the type is a LineString. I don't know why.
            if type(intercept) != LineString:
                # Numba wants me to use a typed list
                typed_list = List()
                [typed_list.append((x[0], x[1])) for x in get_torch_polygon(game_state)]
                # If it's within the torch polygon, draw it red. Otherwise, draw it green.
                if within_polygon((int(intercept.x)), int(intercept.y), typed_list, 2):
                    pygame.draw.circle(game_state.screen, "red", ((int(intercept.x)), (int(intercept.y))), 5)
                else:
                    pygame.draw.circle(game_state.screen, "green", ((int(intercept.x)), (int(intercept.y))), 5)