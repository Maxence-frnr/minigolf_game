import pygame as py
import math
from pygame import Vector2

class Button:
    def __init__(self, text:str="", rect:py.Rect=py.Rect(0, 0, 10, 10), font_size:int=24, color:py.Color=(255, 255, 255), hover_color:py.Color=(200, 200, 200), action=None, action_arg=None, sprite=None, border:bool=False, border_width:int=3, border_radius:int=3, sound=None, sounds_manager = None):
        self.text = text
        self.rect = rect
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.action_arg = action_arg
        self.sprite = sprite
        self.font = py.font.Font(None, font_size)
        self.border = border
        self.border_width = border_width
        self.border_radius = border_radius
        self.sounds_manager = sounds_manager
        if sound and sounds_manager:
            self.sound = self.sounds_manager.get(sound)
        
        self.is_hovered = False

        self.border_rect = rect.copy()
        self.sprite_rect = rect.copy()
        self.border_rect.center = (rect[0], rect[1]) #Centre la bordure autour de pos_x/ pos_y
        if self.sprite:
            self.sprite_rect[0] -= self.sprite.get_rect()[2]//2 #centre le rectangle du sprite autour de pos_x/ pos_y
            self.sprite_rect[1] -= self.sprite.get_rect()[3]//2  
        
    def draw(self, screen:py.Surface):
        if self.border:
            py.draw.rect(screen, self.color, self.border_rect, 3, 3)
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
                if self.text == "Next":
                    print(self.action_arg)
                self.action(self.action_arg)
                if self.sounds_manager:
                    py.mixer.Sound(self.sound).play()


class Wall_old():
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
    
class Wall():
    def __init__(self, start:tuple, end:tuple, width:int, color:tuple):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
    
    def draw(self, screen):
        py.draw.line(screen, self.color, self.start, self.end, self.width)
    
    def detect_and_handle_collision(self, player_pos, player_radius, velocity:Vector2):
        A = Vector2(self.start)
        B = Vector2(self.end)
        C = Vector2(player_pos)
        P = Vector2()#Point le plus proche du joueur sur la droite A-B

        t = ((C - A) * (B - A)) / ((B - A) * (B - A))

        if t < 0: P = A
        elif t > 1: P = B
        else:
            P = A + t*(B - A)
        distance = C.distance_to(P)
        if distance < player_radius:
            normal = (C-P).normalize()

            new_velocity = velocity - 2 * velocity.dot(normal) * normal
            return True, new_velocity
        return False, velocity 

class Ground():
    def __init__(self, rect:py.Rect, type):
        self.rect = rect
        if type == "sand":
            self.color = (255, 255, 0)
            self.friction = 600
        
        elif type == "ice":
            self.color = (0, 255, 255)
            self.friction = 100
        
        elif type == "boost":
            self.color = (222, 76, 18)
            self.friction = -100

    def draw(self, screen):
        py.draw.rect(screen, self.color, self.rect)

    def detect_collision(self, player_pos):
        return self.rect.collidepoint(player_pos)

    def handle_collision(self, player_velocity:Vector2, dt):
        friction_v = player_velocity.normalize() * -self.friction * dt
        player_velocity += friction_v
        return player_velocity
        