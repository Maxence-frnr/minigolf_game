import pygame as py

class Hole:
    def __init__(self, pos:tuple, sprite):
        self.sprite = sprite
        self.pos = py.Vector2(pos[0], pos[1])
        self.rect = self.sprite.get_rect(center = self.pos)

    def draw(self, screen):
        
        screen.blit(self.sprite, self.rect)