import pygame as py
import math
from pygame import Vector2
from state_manager import BaseState
from utils import Button
from player import Player

class Game(BaseState):
    def __init__(self, state_manager, assets_manager):
        self.state_manager = state_manager
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        self.player = Player((300, 300))
        self.max_strength = 600.0
        self.strength = None
        self.builded_strength = Vector2(0, 0)
        self.building_strength_factor = 5.0
        self.friction = 200
        
        self.is_left_button_down = False
        self.is_building_strength = False
        
        #UI
        self.back_to_menu_button_sprite = assets_manager.get("back_arrow")
        
        self.back_to_menu_button = Button("", (10, 10, 30, 30), 10, (255, 255, 255), (255, 0, 0), self.back_to_menu, self.back_to_menu_button_sprite)
        self.buttons = [self.back_to_menu_button]
        
        

    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
    def update(self, dt)->None:
        self.update_player_pos(dt)

    def draw(self, screen):
        screen.fill((50, 50, 50))
        self.player.draw(screen)
        
        #UI
        self.back_to_menu_button.draw(screen)
        if self.builded_strength != Vector2(0, 0):
            self.update_strength_bar(screen)
        
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                self.is_left_button_down = True
                
                if abs(event.pos[0] - self.player.pos[0]) < 10 and abs(event.pos[1] - self.player.pos[1]) < 10:
                    self.is_building_strength = True
                    
            elif event.type == py.MOUSEBUTTONUP:
                self.is_left_button_down = False
                self.is_building_strength = False
                if self.builded_strength.length() > 0:
                    self.strength = self.builded_strength
                self.builded_strength = Vector2(0, 0)
                
            elif event.type == py.MOUSEMOTION:
                if self.is_left_button_down and self.is_building_strength:
                    self.build_strength(event.pos)
                    
    
    def update_player_pos(self, dt): #Calc physics of the player
        if self.strength and self.strength.length() > 0:
            self.player.v += self.strength

        if self.player.v.length() > 0:
            friction_v = self.player.v.normalize() * -self.friction
            self.player.v += friction_v * dt

        self.strength = Vector2(0, 0)
        
        player_next_pos = self.player.pos + self.player.v * dt
        #inverse player velocity if player is out of bounds
        if player_next_pos[0] < 0 or player_next_pos[0] > self.WIDTH:
            self.player.v.x = -self.player.v.x
            player_next_pos.x = max(0, min(self.WIDTH, player_next_pos.x))

        if player_next_pos[1] < 0 or player_next_pos[1] > self.HEIGHT:
            self.player.v.y = -self.player.v.y
            player_next_pos.y = max(0, min(self.HEIGHT, player_next_pos.y))
            
        self.player.pos = player_next_pos
        
    def back_to_menu(self):
        self.state_manager.set_state("menu")
        
    def build_strength(self, pos):
        strength_x = min(abs(self.building_strength_factor*(pos[0] - self.player.pos[0])), self.max_strength)
        strength_y = min(abs(self.building_strength_factor*(pos[1] - self.player.pos[1])), self.max_strength)
        if pos[0] - self.player.pos[0] > 0:
            strength_x = -strength_x
        if pos[1] - self.player.pos[1] > 0:
            strength_y = -strength_y
            
        self.builded_strength = Vector2(strength_x, strength_y)
        print(self.builded_strength)
        
    def update_strength_bar(self, screen):
        builded_strength_length = max(abs(self.builded_strength[0]), abs(self.builded_strength[1]))
        builded_strength_bar = (self.player.pos[0] + 20, self.player.pos[1] + 5 -abs(builded_strength_length/20) , 7, abs(builded_strength_length/20))
        max_builded_strength_bar = (self.player.pos[0] + 20 - 1, self.player.pos[1] + 5 - 600/20-2, 9, 600/20+4)
        
        if builded_strength_length <= 200:
            color = (0, 255, 0)
        elif 200 <= builded_strength_length < 450:
            color = (255, 200, 0)
        else:
            color = (255, 0, 0)
        py.draw.rect(screen, (150, 155, 155), max_builded_strength_bar)
        py.draw.rect(screen, color, builded_strength_bar)
        
        