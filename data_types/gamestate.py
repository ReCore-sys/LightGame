import pygame
from numba.experimental import jitclass
from pygame import Surface
from pygame.key import ScancodeWrapper
from pygame.time import Clock


class DebugInfo:
    frame_time: int = 0
    fps: int = 0
    sleep_time: int = 0
    last_pos: [int, int] = [0, 0]
    last_time: int = 0
    advanced_debug: bool = False


class Config:
    framerate: int = 120
    view_distance: int = 500
    view_angle: int = 15


class MapNode:
    start_x: int = 0
    start_y: int = 0
    end_x: int = 0
    end_y: int = 0

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y


class Map:
    Nodes: list[MapNode] = []
    UniquePoints: list[pygame.Vector2] = []

class GameState:
    screen: Surface
    clock: Clock
    dt: int
    close: bool
    player_pos: pygame.Vector2
    pressed: ScancodeWrapper
    fps_counter = 0
    show_debug = False
    debug_info: DebugInfo = DebugInfo()
    config: Config = Config()
    map: Map = Map()

    def __init__(self, screen: Surface, clock: Clock):
        self.screen = screen
        self.clock = clock
        self.dt = 0
        self.close = False