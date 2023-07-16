import math

import pygame
from numba.typed import List
from pygame import Vector2
from shapely.geometry import LineString

from data_types.gamestate import GameState
from game.gamestates.main.torch import get_torch_polygon
from utils.vector_stuffs import within_polygon


def sort_points(points: List[Vector2]) -> List[Vector2]:
    center = Vector2(0, 0)
    for p in points:
        center += p
    center /= len(points)

    angles = [math.atan2(p.y - center.y, p.x - center.x) for p in points]

    sorted_points = [p for _, p in sorted(zip(angles, points))]

    return sorted_points


def draw_to_map_nodes(game_state: GameState):
    # polygon = compute_polygon(game_state)
    torch_poly = get_torch_polygon(game_state)
    pygame.draw.polygon(game_state.screen, "white", torch_poly, 1)

    # # Draw all the intersections of the blue lines and the map nodes
    # for node in game_state.map.Nodes:
    #     # Using shapely to find the intersection because I am stupid and can't do it myself
    #     line = LineString([(game_state.player_pos.x, game_state.player_pos.y), (point[0], point[1])])
    #     other_line = LineString([(node.start_x, node.start_y), (node.end_x, node.end_y)])
    #     intercept: Point = line.intersection(other_line)
    #     # If there is no intersection, the type is a LineString. I don't know why.
    #     if type(intercept) != LineString:
    #         # Numba wants me to use a typed list
    #         typed_list = List()
    #         [typed_list.append((x[0], x[1])) for x in get_torch_polygon(game_state)]
    #         # If it's within the torch polygon, draw it red. Otherwise, draw it green.
    #         if within_polygon((int(intercept.x)), int(intercept.y), typed_list):
    #             pygame.draw.circle(game_state.screen, "red", ((int(intercept.x)), (int(intercept.y))), 5)
    #             # Find all unique points within the torch polygon
    #             anyintersect = False
    #             for unique_point in game_state.map.UniquePoints:
    #                 view_vector = Vector2(unique_point.x - game_state.player_pos.x,
    #                                       unique_point.y - game_state.player_pos.y)
    #                 view_vector.scale_to_length(game_state.config.view_distance)
    #                 if within_polygon(unique_point.x, unique_point.y, typed_list):
    #                     anyintersect = True
    #                     # Draw a line from the player to the unique point, extended to the view distance
    #
    #                     # Do a similar thing, but extend a line from the unique point to intercept
    #                     unique_vector = Vector2(intercept.x - unique_point.x, intercept.y - unique_point.y)
    #                     if unique_vector.length() != 0:
    #                         unique_vector.scale_to_length(game_state.config.view_distance)
    #
    #                     nosee_polygon = [
    #                         (unique_vector.x + unique_point.x, unique_vector.y + unique_point.y),
    #                         (intercept.x, intercept.y),
    #                         (unique_point.x, unique_point.y),
    #                         (game_state.player_pos.x + view_vector.x,
    #                          game_state.player_pos.y + view_vector.y)
    #                     ]
    #                 if not anyintersect:
    #                     viewline1 = LineString([(game_state.player_pos.x, game_state.player_pos.y),
    #                                             get_torch_polygon(game_state)[0]])
    #                     viewline2 = LineString([(game_state.player_pos.x, game_state.player_pos.y),
    #                                             get_torch_polygon(game_state)[1]])
    #                     edgeview = LineString([get_torch_polygon(game_state)[0], get_torch_polygon(game_state)[1]])
    #                     if viewline1.intersects(other_line) and viewline2.intersects(other_line):
    #                         anyintersect = True
    #                         nosee_polygon = [
    #                             (viewline1.intersection(other_line).x, viewline1.intersection(other_line).y),
    #                             (viewline2.intersection(other_line).x, viewline2.intersection(other_line).y),
    #                             (get_torch_polygon(game_state)[1][0], get_torch_polygon(game_state)[1][1]),
    #                             (get_torch_polygon(game_state)[0][0], get_torch_polygon(game_state)[0][1]),
    #                         ]
    #                     elif edgeview.intersects(other_line):
    #                         anyintersect = True
    #                         # Find which corner of the torch polygon is closest to the intersection
    #                         closest_corner: Vector2
    #                         if math.hypot(get_torch_polygon(game_state)[0][0] - intercept.x,
    #                                       get_torch_polygon(game_state)[0][1] - intercept.y) < \
    #                                 math.hypot(get_torch_polygon(game_state)[1][0] - intercept.x,
    #                                            get_torch_polygon(game_state)[1][1] - intercept.y):
    #                             closest_corner = Vector2(get_torch_polygon(game_state)[0][0],
    #                                                      get_torch_polygon(game_state)[0][1])
    #                         else:
    #                             closest_corner = Vector2(get_torch_polygon(game_state)[1][0],
    #                                                      get_torch_polygon(game_state)[1][1])
    #                         nosee_polygon = [
    #                             (edgeview.intersection(other_line).x, edgeview.intersection(other_line).y),
    #                             (closest_corner.x, closest_corner.y),
    #                             (intercept.x, intercept.y)
    #                         ]
    #                 if anyintersect:
    #                     pygame.draw.polygon(game_state.screen, "purple", nosee_polygon)
    #         else:
    #             pygame.draw.circle(game_state.screen, "green", ((int(intercept.x)), (int(intercept.y))), 5)
    edgepoints = List()
    edgepoints.append((get_torch_polygon(game_state)[0][0], get_torch_polygon(game_state)[0][1]))
    edgepoints.append((get_torch_polygon(game_state)[1][0], get_torch_polygon(game_state)[1][1]))
    edgepoints.append((game_state.player_pos.x, game_state.player_pos.y))
    max_x, max_y, min_x, min_y = 0, 0, 99999, 99999
    for point in edgepoints:
        if point[0] > max_x:
            max_x = point[0]
        if point[0] < min_x:
            min_x = point[0]
        if point[1] > max_y:
            max_y = point[1]
        if point[1] < min_y:
            min_y = point[1]
    pygame.draw.rect(game_state.screen, "yellow", (min_x, min_y, max_x - min_x, max_y - min_y), 1)
    # find the furthest box corner from the player
    corners = List()
    corners.append((min_x, min_y))
    corners.append((max_x, min_y))
    corners.append((max_x, max_y))
    corners.append((min_x, max_y))
    box_lines = []
    for i in range(0, 4):
        box_lines.append(LineString([corners[i], corners[(i + 1) % 4]]))
    for unique in game_state.map.UniquePoints:
        if within_polygon(unique.x, unique.y, corners):
            pygame.draw.circle(game_state.screen, "green", (int(unique.x), int(unique.y)), 10)
            vector_to_point = Vector2(unique.x - game_state.player_pos.x, unique.y - game_state.player_pos.y)
            vector_to_point.scale_to_length(game_state.config.view_distance * 1.5)
            pygame.draw.aaline(game_state.screen, "green", (unique.x, unique.y),
                               (game_state.player_pos.x + vector_to_point.x,
                                game_state.player_pos.y + vector_to_point.y))
            draw_poly = [(game_state.player_pos.x + vector_to_point.x,
                          game_state.player_pos.y + vector_to_point.y), (unique.x, unique.y)]

            for node in game_state.map.Nodes:
                if node.start_x == unique.x and node.start_y == unique.y:
                    pygame.draw.line(game_state.screen, "green", (unique.x, unique.y),
                                     (node.end_x, node.end_y), 5)
                    draw_poly.append((node.end_x, node.end_y))
                elif node.end_x == unique.x and node.end_y == unique.y:
                    pygame.draw.line(game_state.screen, "green", (unique.x, unique.y),
                                     (node.start_x, node.start_y), 5)
                    draw_poly.append((node.start_x, node.start_y))

            if len(draw_poly) > 2:
                # sort draw_poly by how close each point is to the player
                draw_poly.sort(key=lambda x: math.hypot(x[0] - game_state.player_pos.x,
                                                        x[1] - game_state.player_pos.y))
                pygame.draw.polygon(game_state.screen, "purple", draw_poly)

    for node in game_state.map.Nodes:
        nodeline = LineString([(node.start_x, node.start_y), (node.end_x, node.end_y)])
        draw_poly = []
        if nodeline.intersects(box_lines[0]) and nodeline.intersects(box_lines[2]):
            intersect1 = nodeline.intersection(box_lines[0])
            intersect2 = nodeline.intersection(box_lines[2])
            pygame.draw.circle(game_state.screen, "green", (int(intersect1.x), int(intersect1.y)), 10)
            pygame.draw.circle(game_state.screen, "green", (int(intersect2.x), int(intersect2.y)), 10)
            draw_poly.append(Vector2(intersect1.x, intersect1.y))
            draw_poly.append(Vector2(intersect2.x, intersect2.y))
            draw_poly.append(Vector2(torch_poly[1][0], torch_poly[1][1]))
            draw_poly.append(Vector2(torch_poly[0][0], torch_poly[0][1]))
        if nodeline.intersects(box_lines[1]) and nodeline.intersects(box_lines[3]):
            intersect1 = nodeline.intersection(box_lines[1])
            intersect2 = nodeline.intersection(box_lines[3])
            draw_poly.append(Vector2(intersect1.x, intersect1.y))
            draw_poly.append(Vector2(intersect2.x, intersect2.y))
            draw_poly.append(Vector2(torch_poly[1][0], torch_poly[1][1]))
            draw_poly.append(Vector2(torch_poly[0][0], torch_poly[0][1]))
        if len(draw_poly) > 3:
            # Sort draw_poly by how close each point is to the player
            draw_poly = sort_points(draw_poly)
            pygame.draw.polygon(game_state.screen, "pink", draw_poly)