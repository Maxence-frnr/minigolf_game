import pygame as py

class Player:
    def __init__(self, pos:tuple, radius, sprite):
        self.radius = radius
        self.pos = py.Vector2(pos[0], pos[1])
        self.v = py.Vector2(0, 0)
        self.sprite = sprite
        self.rect = self.sprite.get_rect(center = self.pos)

    def draw(self, screen): 
        #py.draw.circle(screen, "white", self.pos, self.radius)
        self.rect = self.sprite.get_rect(center = self.pos)
        screen.blit(self.sprite, self.rect)