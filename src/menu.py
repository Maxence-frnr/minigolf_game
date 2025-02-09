import pygame as py
from state_manager import BaseState
from utils import Button

class MenuState(BaseState):
    def __init__(self, state_manager):
        self.state_manager = state_manager
        #UI elements to enable
        self.title_font = py.font.Font(None, 100)
        
        
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
        self.play_button = Button("Play", py.Rect(self.WIDTH//2, self.HEIGHT//2, 100, 60),60, (210, 210, 210), (255, 255, 255), self.play, border=True)
        self.buttons = [self.play_button]
        
    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()

    def draw(self, screen):
        screen.fill((50, 50, 50))
        self.play_button.draw(screen)
        title_surface = self.title_font.render("Mini Golf 2D", True, (255, 255, 255))
        title_surface_pos_x = self.WIDTH//2 - title_surface.get_width()//2
        title_surface_pos_y = self.HEIGHT//2- 175
        screen.blit(title_surface, (title_surface_pos_x, title_surface_pos_y))
    
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
            
    def play(self, *args):
        self.state_manager.set_state(name="level_selection_menu")#, level="level_1"