import pygame
import sqlite3

from pygame import Vector2

from data_types.gamestate import GameState, MapNode


def preload(game_state: GameState):
    db = sqlite3.connect("walls.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM walls")
    walls = cursor.fetchall()
    for wall in walls:
        game_state.map.Nodes.append(MapNode(wall[0], wall[1], wall[2], wall[3]))
    cursor.close()
    db.close()
    temp = []
    for node in game_state.map.Nodes:
        temp.append([node.start_x, node.start_y])
        temp.append([node.end_x, node.end_y])
    temp = list(set(tuple(sub) for sub in temp))
    game_state.map.UniquePoints = [Vector2(x[0], x[1]) for x in temp]


def draw_map(game_state: GameState):
    for node in game_state.map.Nodes:
        pygame.draw.aaline(game_state.screen, "white", (node.start_x, node.start_y), (node.end_x, node.end_y), 5)