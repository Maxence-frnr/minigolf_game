import pygame as py
import random as r
from pygame import Vector2
import assets_manager

class Camera:
    def __init__(self):
        self.offset = Vector2(0, 0)
        self.shake_intensity = 0 #intensité actuelle du shake
        self.decay = 0.9 #réduction du shake par frame
        self.min_shake = 0.5
        
    def start_shake(self, intensity:float):#length en secondes
        self.shake_intensity = intensity
    
    def update(self):
        if self.shake_intensity > 0:
            self.offset.x = r.uniform(-self.shake_intensity, self.shake_intensity)
            self.offset.y = r.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity *= self.decay  # Réduction progressive du shake
            if self.shake_intensity < 0.5:  # Seuil minimal pour arrêter le shake
                self.shake_intensity = 0
        else:
            self.offset = Vector2(0, 0)
            
        
class Button:
    def __init__(self, text:str="", rect:py.Rect=py.Rect(0, 0, 10, 10), font_size:int=24, color:py.Color=(255, 255, 255), hover_color:py.Color=(200, 200, 200), action=None, action_arg=None, sprite=None, border:bool=False, border_width:int=3, border_radius:int=3, sound=None):
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
        if sound:
            self.sound = assets_manager.get_sound(sound)
        else:
            self.sound = False
        
        self.is_hovered = False

        self.border_rect = rect.copy()
        self.sprite_rect = rect.copy()
        self.border_rect.center = (rect[0], rect[1]) #Centre la bordure autour de pos_x/ pos_y
        if self.sprite:
            self.sprite_rect[0] -= self.sprite.get_rect()[2]//2 #centre le rectangle du sprite autour de pos_x/ pos_y
            self.sprite_rect[1] -= self.sprite.get_rect()[3]//2  
        
    def draw(self, screen:py.Surface):
        if self.border:
            py.draw.rect(screen, self.color, self.border_rect, self.border_width, 3)
        color = self.hover_color if self.is_hovered else self.color
        if self.sprite: screen.blit(self.sprite, self.sprite_rect)
        text = self.font.render(self.text, True, color)
        text_rect = text.get_rect(center= (self.rect[0], self.rect[1]))
        screen.blit(text, text_rect)
        
        
    def handle_events(self, events:py.event.Event):
        for event in events:
            if event.type == py.MOUSEMOTION:
                self.is_hovered = py.Rect.collidepoint(self.border_rect, event.pos)
            elif event.type == py.MOUSEBUTTONDOWN and self.is_hovered and py.mouse.get_pressed()[0]:
                self.action(self.action_arg)
                if self.sound:
                    py.mixer.Sound(self.sound).play()
    
    
class Div:
    def __init__(self, rect:py.Rect, border:bool=False, color=(255, 255, 255), hover_color=None, border_radius:int=3, border_width:int = 3):
        self.rect = rect
        self.rect.center = (rect[0], rect[1])
        self.childs = {}
        self.border = border
        self.color = color
        self.hover_color = color
        self.border_radius = border_radius
        self.border_width = border_width
        
    def draw(self, screen):
        py.draw.rect(screen, self.color, self.rect, self.border_width, self.border_radius)
        for child in self.childs:
            child.draw(screen)
        
    def add_child(self, child):
        pass
    
    def remove_child(self, name=None, index=None):
        pass
    
    def remove_all_child(self):
        pass


class Label:
    def __init__(self, text:str="", rect:py.Rect=py.Rect(0, 0, 10, 10), font_size:int=24, color:py.Color=(255, 255, 255), sprite=None, border:bool=False, border_width:int=3, border_radius:int=3):
        self.text = text
        self.rect = rect
        self.font_size = font_size
        self.color = color

        self.sprite = sprite
        self.font = py.font.Font(None, font_size)
        self.border = border
        self.border_width = border_width
        self.border_radius = border_radius
        

        self.border_rect = rect.copy()
        self.sprite_rect = rect.copy()
        self.border_rect.center = (rect[0], rect[1]) #Centre la bordure autour de pos_x/ pos_y
        if self.sprite:
            self.sprite_rect[0] -= self.sprite.get_rect()[2]//2 #centre le rectangle du sprite autour de pos_x/ pos_y
            self.sprite_rect[1] -= self.sprite.get_rect()[3]//2  
        
    def draw(self, screen:py.Surface):
        color = self.color
        if self.border:
            py.draw.rect(screen, color, self.border_rect, self.border_width, 3)
        if self.sprite: screen.blit(self.sprite, self.sprite_rect)
        text = self.font.render(self.text, True, color)
        text_rect = text.get_rect(center= (self.rect[0], self.rect[1]))
        screen.blit(text, text_rect)
    
    def handle_events(self, events:py.event.Event):
        pass
      
          
class Particle(py.sprite.Sprite):
    def __init__(self, 
                groups: py.sprite.Group, 
                pos: Vector2, 
                color: tuple, 
                speed: Vector2,
                size:int,
                sprite: py.image=None):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.speed = speed
        self.sprite = sprite
        self.size = size
        if self.sprite:
            self.size = self.sprite.get_width()

        self.get_surface()

    def get_surface(self):
        self.image = py.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=self.pos)
        if self.sprite:
            sprite_rect = self.sprite.get_rect(center = (self.size//2,self.size//2))
            self.image.blit(self.sprite, sprite_rect)
        else:
            #py.draw.circle(self.image, self.color, center=(self.size//2, self.size//2), radius=self.size//2)
            py.draw.rect(self.image, self.color, py.Rect(0, 0, self.size, self.size))
        

    def move(self, dt):
        self.pos += self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.move(dt)


class Player_Particle(Particle):
    def __init__(self, 
                 groups:py.sprite.Group, 
                 pos, 
                 color,  
                 speed:Vector2,
                 sprite:py.image = None):
        k1 = r.uniform(-0.4, 0.4)
        k2 = k1 = r.uniform(-0.4, 0.4)
        speed = py.Vector2(speed[0] +k1 , speed[1] + k2).normalize()
        size = r.randint(2, 8)
        
        super().__init__(groups, pos, color, speed, size, sprite)
        
        self.scale = 1
        self.alpha = 255
        self.angle = r.randint(0, 359)

        self.inflate_speed = 5
        self.fade_speed = 400
        self.rotation_speed = round(r.uniform(-1, 1))
        self.slow_factor = 1.1

        self.max_size = 20
        self.min_speed = 1
        #self.image = py.transform.rotate(self.image, self.angle)
        #self.rect = self.image.get_rect(center=self.pos)
        #self.size = self.sprite.get_width()

    def slow(self, dt):
        if self.speed.length() > self.min_speed:
            self.speed *= self.slow_factor * dt


    def rotate(self, dt):
        self.angle += self.rotation_speed * dt
        self.image = py.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center = self.pos)

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def inflate(self, dt):
        if self.size < self.max_size:
            self.size += self.inflate_speed * dt
            self.get_surface()

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.inflate(dt)
        self.rotate(dt)
        self.fade(dt)
        self.slow(dt)
        
        self.check_alpha()


class HoleInOneParticule(Particle):
    def __init__(self,
                 groups:py.sprite.Group,
                 pos,
                 color,
                 speed,
                 size):
        self.lifetime = 0.3 # in seconds
        self.g = Vector2(0, 1000)

        super().__init__(groups, pos, color, speed, size)
    
    def decay(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def gravity(self, dt):
        self.speed += self.g * dt

    def update(self, dt):
        self.decay(dt)
        self.gravity(dt)
        self.move(dt)