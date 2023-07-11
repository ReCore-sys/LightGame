import pygame
from pygame import Surface
from pygame.key import ScancodeWrapper
from pygame.time import Clock


class GameState:
    screen: Surface
    clock: Clock
    dt: int
    close: bool
    player_pos: pygame.Vector2
    pressed: ScancodeWrapper
    rerender = True
    fps_counter = 0

    def __init__(self, screen: Surface, clock: Clock):
        self.screen = screen
        self.clock = clock
        self.dt = 0
        self.close = False