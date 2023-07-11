import pygame

from data_types.gamestate import GameState

move_speed = 200

X = 60
Y = 16

font = pygame.font.Font('freesansbold.ttf', 16)

player_pos: pygame.Vector2
rerender = True
fps_text = "0 FPS"
fps_counter = 0


def preload(game_state: GameState):
    game_state.player_pos = pygame.Vector2(game_state.screen.get_width() / 2, game_state.screen.get_height() / 2)
    game_state.screen.fill("black")
    return game_state


def update(game_state: GameState):
    global fps_text

    # The main loop in the root handles the fetching of key presses, so we don't need to do it here
    # To optimize, we first check if any keys we care about are pressed, and only then do we do the math
    if any([game_state.pressed[pygame.K_w], game_state.pressed[pygame.K_s], game_state.pressed[pygame.K_a],
            game_state.pressed[pygame.K_d]]):
        # Create an empty vector, then add to it based on which keys are pressed
        move = pygame.Vector2(0, 0)
        if game_state.pressed[pygame.K_w]:
            move.y -= move_speed * (game_state.dt / 1000)
        if game_state.pressed[pygame.K_s]:
            move.y += move_speed * (game_state.dt / 1000)
        if game_state.pressed[pygame.K_a]:
            move.x -= move_speed * (game_state.dt / 1000)
        if game_state.pressed[pygame.K_d]:
            move.x += move_speed * (game_state.dt / 1000)
        game_state.player_pos += move
        # Something has changed, so we need to rerender
        game_state.rerender = True

    # Only draw the fps every 240 frames, to reduce the amount of work we do
    # This is not an amazing way of doing it since it'll get fucky at lower frame rates, but it works for now
    game_state.fps_counter += 1
    if game_state.fps_counter == 120:
        game_state.fps_counter = 0
        try:
            fps_text = str(round(game_state.clock.get_fps()) if game_state.clock.get_fps() < 1000 else "-") + " FPS"
        except OverflowError:
            fps_text = "-"
        game_state.rerender = True

    # Increase the stored tick
    game_state.dt = game_state.clock.tick()
    # If we need to rerender the screen
    if game_state.rerender:
        pygame.draw.circle(game_state.screen, "red", game_state.player_pos, 10)
        pygame.display.update()
        # Now a bunch of post render stuff
        game_state.screen.fill("black")
        text = font.render(fps_text, True, (0, 255, 0), None)
        text_rect = text.get_rect()
        text_rect.center = ((X + len(fps_text) * 2) // 2, Y // 2)
        game_state.screen.blit(text, text_rect)

        # Check if we have closed the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.close = True
        game_state.rerender = False
    return game_state