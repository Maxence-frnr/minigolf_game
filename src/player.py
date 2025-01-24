import pygame as py

class Player:
    def __init__(self, pos:tuple):
        self.sprite = (7)
        self.pos = py.Vector2(pos[0], pos[1])
        self.v = py.Vector2(0, 0)

    def draw(self, screen): 
        py.draw.circle(screen, "white", self.pos, self.sprite)