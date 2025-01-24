import pygame as py
from state_manager import StateManager
from menu import MenuState
from game import Game

#CONSTANT
WIDTH, HEIGHT = 1280, 720


py.init()
screen = py.display.set_mode((WIDTH, HEIGHT), flags=py.RESIZABLE)
clock = py.time.Clock()

#state initialisation
state_manager = StateManager()
menu_state = MenuState()
game_state = Game()
state_manager.add_state("menu", menu_state)
state_manager.add_state("game", game_state)


state_manager.set_state("game")

running = True
while running:
    dt = clock.tick(60) / 1000

    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
        elif event.type == py.WINDOWSIZECHANGED:
            state_manager.current_state.update_window_size(screen)
    
    state_manager.handle_events(events)
    state_manager.update(dt)
    state_manager.draw(screen)

    py.display.flip()

py.quit()