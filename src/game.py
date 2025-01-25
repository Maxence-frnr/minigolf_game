import pygame as py
from pygame import Vector2
from state_manager import BaseState
from utils import Button
from player import Player

class Game(BaseState):
    def __init__(self, state_manager, assets_manager):
        self.state_manager = state_manager
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        self.player = Player((300, 300))
        self.strength = Vector2(300.0, 300.0)
        self.friction = 100
        
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
        
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
    
    def update_player_pos(self, dt): #Calc physics of the player
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
