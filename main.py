# Example file showing a circle moving on screen
import pygame
from pygame.locals import DOUBLEBUF

from data_types.gamestate import GameState

flags = DOUBLEBUF

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), flags, 16)
clock = pygame.time.Clock()
running = True
dt = 0
screen.set_alpha(None)

gamestate = GameState(screen, clock)
from game.gamestates.main.main import preload

gamestate = preload(gamestate)

while gamestate.close is False:
    from game.gamestates.main.main import update

    gamestate.pressed = pygame.key.get_pressed()
    gamestate = update(gamestate)

pygame.quit()