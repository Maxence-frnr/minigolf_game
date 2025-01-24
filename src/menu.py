import pygame as py
from state_manager import BaseState

class MenuState(BaseState):
    def __init__(self):
        #UI elements to enable
        self.title_font = py.font.Font(None, 50)
        self.buttons = ["Play", "Settings", "Quit"]
        self.WIDTH, self.HEIGHT = py.display.get_window_size()

    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()

    def draw(self, screen):
        screen.fill((0, 0, 0))

        title_surface = self.title_font.render("Mini Golf 2D", True, (255, 255, 255))
        title_surface_pos_x = self.WIDTH//2 - title_surface.get_width()//2
        title_surface_pos_y = self.HEIGHT//2  - title_surface.get_height()//2
        screen.blit(title_surface, (title_surface_pos_x, title_surface_pos_y))
    
