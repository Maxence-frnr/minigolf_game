import pygame as py
from state_manager import BaseState
from utils import Button

class LevelSelectionMenu(BaseState):
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.title_font = py.font.Font(None, 50)
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
        self.level_cards = []
        #self.level_cards.append(LevelCard((300,500), 1, 10, self.level_selected))
        rect= py.Rect(200, 500, 75, 75)
        self.level_cards.append(Button("1", rect, 75, border=True, action=self.level_selected, action_arg=1))
        
        rect2= py.Rect(400, 500, 75, 75)
        self.level_cards.append(Button("2", rect2, 75, border=True, action=self.level_selected, action_arg=2))

    def draw(self, screen):
        screen.fill((50, 50, 50))
        for card in self.level_cards:
            card.draw(screen)
    
    def level_selected(self, index):
        print("called")
        self.state_manager.set_state(name="game", level=f"level_{index}")
    
    def handle_events(self, events):
        for card in self.level_cards:
            card.handle_events(events)
    

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
        