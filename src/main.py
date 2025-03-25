import pygame as py

import assets_manager
from state_manager import StateManager
from level_manager import LevelManager
from save_manager import SaveManager

from menu import MenuState
from game import Game
from level_selection_menu import LevelSelectionMenu


#CONSTANT
WIDTH, HEIGHT = 800, 1000
FPS = 120 #plus les fps sont élevés, meilleurs sont les collisions

py.init()
py.mixer.init()
screen = py.display.set_mode((WIDTH, HEIGHT)) #flags=py.RESIZABLE
py.display.set_caption("Minigolf 2D")
py.display.set_icon(py.image.load("assets\\sprites\\hole.png"))
clock = py.time.Clock()

assets_manager.load_all_assets()

#state initialisation
state_manager = StateManager()

level_manager = LevelManager('data\\levels.json')#automaticaly load all levels from the json
save_manager = SaveManager('data\\data.json')#load all saved data in data.json

menu_state = MenuState(state_manager)
level_selection_menu_state = LevelSelectionMenu(state_manager, save_manager, level_manager)
game_state = Game(state_manager,  level_manager, save_manager)
state_manager.add_state("menu", menu_state)
state_manager.add_state("level_selection_menu", level_selection_menu_state)
state_manager.add_state("game", game_state)

state_manager.set_state(name="menu")

running = True
while running:
    dt = clock.tick(FPS) / 1000

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