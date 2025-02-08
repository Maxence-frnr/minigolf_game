import pygame as py

from assets_manager import AssetsManager
from assets_manager import SoundsManager
from state_manager import StateManager
from level_manager import LevelManager

from menu import MenuState
from game import Game
from level_selection_menu import LevelSelectionMenu

#CONSTANT
WIDTH, HEIGHT = 600, 1000


py.init()
py.mixer.init()
screen = py.display.set_mode((WIDTH, HEIGHT)) #flags=py.RESIZABLE
py.display.set_caption("Minigolf 2D")
clock = py.time.Clock()

#state initialisation
assets_manager = AssetsManager()
sounds_manager = SoundsManager()
state_manager = StateManager()

ball = assets_manager.load("ball", "assets\\sprites\\16x16 ball.png")
back_arrow = assets_manager.load("back_arrow", "assets\\sprites\\back_arrow.png")
white_arrow = assets_manager.load("white_arrow", "assets\\sprites\\white_arrow_edited.png")
hole = assets_manager.load("hole", "assets\\sprites\\hole.png")

level_manager = LevelManager('data\\levels.json')#automaticaly load all levels from the json

#sound initialisation
swing_sound = sounds_manager.load("swing", "assets\\sounds\\swing.mp3")
bounce_sound = sounds_manager.load("bounce", "assets\\sounds\\bounce.mp3")
hole_sound = sounds_manager.load("hole", "assets\\sounds\\hole.mp3")

menu_state = MenuState(state_manager)
level_selection_menu_state = LevelSelectionMenu(state_manager)
game_state = Game(state_manager, assets_manager, level_manager, sounds_manager)
state_manager.add_state("menu", menu_state)
state_manager.add_state("level_selection_menu", level_selection_menu_state)
state_manager.add_state("game", game_state)


state_manager.set_state(name="menu")

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