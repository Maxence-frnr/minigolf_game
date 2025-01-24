import pygame as py
from pygame import Vector2
from state_manager import BaseState
from player import Player

class Game(BaseState):
    def __init__(self):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        self.player = Player((300, 300))
        self.strengt = Vector2(300.0, 300.0)
        self.friction = 100

    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()

    
    def update(self, dt):
        self.update_player_pos(dt)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.player.draw(screen)
    
    def update_player_pos(self, dt):
        self.player.v += self.strengt

        if self.player.v.length() > 0:  # Vérifier que la vitesse n'est pas nulle pour éviter une division par zéro
            friction_v = self.player.v.normalize() * -self.friction
            self.player.v += friction_v * dt

        self.strengt = Vector2(0, 0)

        player_next_pos = self.player.pos + self.player.v * dt

        if player_next_pos[0] < 0 or player_next_pos[0] > self.WIDTH:
            self.player.v.x = -self.player.v.x
            player_next_pos.x = max(0, min(self.WIDTH, player_next_pos.x))

        if player_next_pos[1] < 0 or player_next_pos[1] > self.HEIGHT:
            self.player.v.y = -self.player.v.y
            player_next_pos.y = max(0, min(self.HEIGHT, player_next_pos.y))

        self.player.pos = player_next_pos
