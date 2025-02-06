import pygame as py
import math

class Button:
    def __init__(self, text, rect:tuple, font_size, color, hover_color, action, sprite=None):
        self.text = text
        self.rect = py.Rect(rect)
        self.font = py.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False
        self.sprite = sprite
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        if self.sprite: screen.blit(self.sprite, self.rect)
        text_surface = self.font.render(self.text, True, color)
        screen.blit(text_surface, self.rect)
        
    def handle_events(self, events):
        for event in events:
            if event.type == py.MOUSEMOTION:
                self.is_hovered = py.Rect.collidepoint(self.rect, event.pos)
            elif event.type == py.MOUSEBUTTONDOWN and self.is_hovered:
                self.action()

class Wall():
    def __init__(self, rect:tuple, color):
        self.rect = rect
        self.color = color

    def draw(self, screen):
        py.draw.rect(screen, self.color, self.rect)

    def detect_collision(self, player_pos, player_radius):
        closest_x = max(self.rect.left, min(player_pos[0], self.rect.right))
        closest_y = max(self.rect.top, min(player_pos[1], self.rect.bottom))

        distance = math.sqrt((player_pos[0]- closest_x)**2 + (player_pos[1]- closest_y)**2)
        return distance < player_radius
    
    def get_penetration_depth(self, player_pos, player_radius):
        penetration_x = 0
        penetration_y = 0

        if player_pos[0] < self.rect.left:
            penetration_x = (player_pos[0] + player_radius) - self.rect.left -1
        elif player_pos[0] > self.rect.right:
            penetration_x = -((player_pos[0] - player_radius) - self.rect.right) + 1

        if player_pos[1] < self.rect.top:
            penetration_y = (player_pos[1] + player_radius) - self.rect.top -1 
        elif player_pos[1] > self.rect.bottom:
            penetration_y = -((player_pos[1] - player_radius) - self.rect.bottom) + 1

        return penetration_x, penetration_y
    
class Wall2():
    def __init__(self, start:tuple, end:tuple, width:int, color:tuple):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
    
    def draw(self, screen):
        py.draw.line(screen, self.color, self.start, self.end, self.width)
