# Example file showing a circle moving on screen
import pygame
from pygame.locals import DOUBLEBUF
import game.gamestates.main.map as map

from data_types.gamestate import GameState, MapNode
from game.gamestates.main import main, debug

flags = DOUBLEBUF

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), flags, 16)
clock = pygame.time.Clock()
running = True
dt = 0
screen.set_alpha(None)

game_state = GameState(screen, clock)

debug.preload(game_state)
main.preload(game_state)
map.preload(game_state)
print(screen.get_size())
while game_state.close is False:
    from game.gamestates.main.main import update

    update(game_state)

pygame.quit()