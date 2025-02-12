import pygame as py
from state_manager import BaseState
from utils import Button

class LevelSelectionMenu(BaseState):
    def __init__(self, state_manager, assets_manager, sounds_manager):
        self.state_manager = state_manager
        self.sounds_manager = sounds_manager
        self.title_font = py.font.Font(None, 50)
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
        self.back_to_menu_button_sprite = assets_manager.get("back_arrow")
        self.buttons = []
        self.buttons.append(Button(text="", rect=py.Rect(30, 30, 30, 30), font_size=10, color=(255, 255, 255), hover_color=(255, 0, 0), action=self.back_to_menu, sprite=self.back_to_menu_button_sprite, sound="click", sounds_manager=sounds_manager))
        
        self.level_cards = []
        self.create_level_cards()
       
    def create_level_cards(self):
        pos_x = 150
        pos_y = 200
        for i in range(1, 16):
            rect = py.Rect(pos_x, pos_y, 75, 75)
            self.level_cards.append(Button(str(i), rect, 75, border=True, action=self.level_selected, action_arg=i, sound="click", sounds_manager=self.sounds_manager))
            pos_x += 150
            if pos_x == 600:
                pos_x = 150
                pos_y += 150


    def draw(self, screen):
        screen.fill((50, 50, 50))
        for button in self.buttons:
            button.draw(screen)
        for card in self.level_cards:
            card.draw(screen)
    
    def level_selected(self, index):
        self.state_manager.set_state(name="game", level=f"level_{index}")
    
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
        for card in self.level_cards:
            card.handle_events(events)
            
    def back_to_menu(self, *args):
        self.state_manager.set_state(name="menu")
    

class LevelCard:
    def __init__(self, pos, index, highscore, function):
        self.font = py.font.Font(None, 20)
        self.pos = pos
        self.index = index
        self.highscore = highscore
        
        self.rect = py.Rect(pos[0], pos[1], 50, 50)
        self.button = Button(str(index), self.rect, 75, (255, 255, 255), (200, 200, 200), function(index))
        self.rect.center = pos
        
    def draw(self, screen):
        self.button.draw(screen)
        py.draw.rect(screen, (200, 100, 200), self.rect, 3, 3)
    
    def handle_events(self, events):
        self.button.handle_events(events)
        