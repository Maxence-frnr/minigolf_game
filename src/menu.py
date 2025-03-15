import pygame as py
from state_manager import BaseState
from utils import Button
from utils import Particle

class MenuState(BaseState):
    def __init__(self, state_manager, sounds_manager):
        self.state_manager = state_manager
        self.sounds_manager = sounds_manager
        #UI elements to enable
        self.title_font = py.font.Font(None, 125)
        
        
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
        self.play_button = Button("Play", py.Rect(self.WIDTH//2, self.HEIGHT//2, 130, 80), 75, (255, 255, 255), (210, 210, 210), self.play, border=True, sounds_manager=sounds_manager, sound="click")
        self.buttons = [self.play_button]

        
    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()

    def draw(self, screen):
        self.draw_background(screen)
        self.play_button.draw(screen)
        title_surface = self.title_font.render("Mini Golf 2D", True, (255, 255, 255))
        title_surface_pos_x = self.WIDTH//2 - title_surface.get_width()//2
        title_surface_pos_y = self.HEIGHT//2- 175
        screen.blit(title_surface, (title_surface_pos_x, title_surface_pos_y))
    
    def draw_background(self, screen):
        CELL_SIZE = 50
        screen.fill((131, 177, 73))
        for i in range(self.WIDTH // CELL_SIZE):
            for j in range (self.HEIGHT // CELL_SIZE):
                if (i + j) %2 == 0:
                    py.draw.rect(screen, (161, 197, 75), (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 0 )
    
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
            
    def play(self, *args):
        self.state_manager.set_state(name="level_selection_menu")#, level="level_1"
        