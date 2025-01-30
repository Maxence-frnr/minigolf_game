import pygame as py

class Hole:
    def __init__(self, pos:tuple, sprite):
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.rect[0], self.rect[1] = pos[0], pos[1]
        self.pos = py.Vector2(pos[0], pos[1])

    def draw(self, screen):
        
        screen.blit(self.sprite, self.rect)