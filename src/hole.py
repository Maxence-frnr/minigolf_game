import pygame as py
from pygame import Vector2

class Hole:
    def __init__(self, pos:Vector2, sprite:py.image):
        self.sprite = sprite
        self.pos = pos
        self.rect = self.sprite.get_rect(center = self.pos)
        self.radius = 15

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
        #py.draw.circle(screen, "red", self.pos, self.radius, 1) 
        
    def detect_collision(self, player_pos:Vector2, player_radius:float):
        d = self.pos.distance_to(player_pos)
        return d < self.radius + player_radius