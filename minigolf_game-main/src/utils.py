import pygame as py

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
