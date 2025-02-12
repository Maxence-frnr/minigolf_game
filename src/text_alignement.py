import pygame as py
py.init()
screen = py.display.set_mode((800, 400))



class Button:
    def __init__(self, text:str="", rect:py.Rect=py.Rect(0, 0, 10, 10), font_size:int=24, color:py.Color=(255, 255, 255), hover_color:py.Color=(200, 200, 200), action=None, sprite=None, border:bool=False, border_width:int=3, border_radius:int=3):
        self.text = text
        self.rect = rect
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.sprite = sprite
        self.font = py.font.Font(None, font_size)
        self.border = border
        self.border_width = border_width
        self.border_radius = border_radius
        
        self.is_hovered = False

        self.sprite_rect = rect.copy()
        self.sprite_rect.center = (rect[0], rect[1])        
        
    def draw(self, screen:py.Surface):
        if self.border:
            py.draw.rect(screen, self.color, self.sprite_rect, 3, 3)
        color = self.hover_color if self.is_hovered else self.color
        if self.sprite: screen.blit(self.sprite, self.sprite_rect)
        text = self.font.render(self.text, True, color)
        text_rect = text.get_rect(center= (self.rect[0], self.rect[1]))
        screen.blit(text, text_rect)
        
        
    def handle_events(self, events:py.event.Event):
        for event in events:
            if event.type == py.MOUSEMOTION:
                self.is_hovered = py.Rect.collidepoint(self.sprite_rect, event.pos)
            elif event.type == py.MOUSEBUTTONDOWN and self.is_hovered:
                self.action()

class LevelCard:
    def __init__(self, pos, index, highscore):
        self.font = py.font.Font(None, 20)
        self.pos = pos
        self.index = index
        self.highscore = highscore
        
        self.rect = py.Rect(pos[0], pos[1], 75, 75)
    
        self.rect.center = pos
        
    def draw(self, screen):
        py.draw.rect(screen, (200, 200, 200), self.rect, 3, 3)
    
    def handle_events(self, events):
        self.button.handle_events(events)

button_rect= py.Rect(500, 200, 75, 75)
def fx(a=None):
    print("called", a)
button = Button("12", button_rect, 75, (255, 255, 255), (150, 0, 255), fx, None, True)
font = py.font.Font(None, 75)
text = font.render("12", True, (255, 255, 255))
text_rect = text.get_rect(center=(300, 200))
card = LevelCard((300, 200), 1, 10)
running  = True
while running:

    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
    screen.fill((0, 0, 0))
    card.draw(screen=screen)
    button.handle_events(events=events)
    button.draw(screen=screen)
    screen.blit(text, text_rect)
    py.draw.circle(screen, (255, 0, 0), (300, 200), 2)
    py.draw.circle(screen, (150, 0, 255), (500, 200), 2)
    py.display.flip()

py.quit()