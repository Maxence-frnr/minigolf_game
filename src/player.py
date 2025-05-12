import pygame as py
from utils import Player_Particle
from pygame import Vector2

class Player:
    def __init__(self, pos:Vector2, radius, sprite:py.sprite.Sprite):
        self.radius = radius
        self.pos = pos
        self.v = Vector2(0, 0)
        self.sprite = sprite
        self.rect = self.sprite.get_rect(center = self.pos)
        self.particle_group = py.sprite.Group()
        
        self.particle_timer = 0
        self.base_interval = 0.2 #en secondes
        
        self.drowning = False
        self.disappearing = False
        self.size = sprite.get_width()
        self.shrink_factor = 10

        self.rolling_on = "default"
        

    def draw(self, screen, offset:Vector2 = Vector2(0, 0)): 
        #py.draw.circle(screen, "white", self.pos, int(self.size*0.5))
        self.rect = self.sprite.get_rect(center = self.pos+ offset)
        screen.blit(self.sprite, self.rect)
        
        self.particle_group.draw(screen)

    def create_particles(self):
        if self.rolling_on == 'default':
            color = (200, 255, 200)
        elif self.rolling_on == 'sand':
            color = (251, 226, 78)
        elif self.rolling_on == 'ice':
            color = (50, 100, 200)
        elif self.rolling_on == 'water':
            color = (54, 127, 220)
        if self.v.length() > 0:
            Player_Particle(groups=self.particle_group,
                 pos=self.pos,
                 color=color,
                 speed= -self.v*1.1)
    
    def update(self, dt:float)-> None:
        self.particle_group.update(dt)
        
        speed = self.v.length()
        scaled_interval = max(self.base_interval / (speed / 300 + 1), 0.07)
        
        self.particle_timer -= dt
        if self.particle_timer <= 0:
            self.create_particles()
            self.particle_timer = scaled_interval
        
        if self.drowning:
            self.drowning_animation(dt)
        
        if self.disappearing:
            self.disappearing_animation(dt)
        
        
            
    def drowning_animation(self, dt):
        if self.v.length() > 2:
            friction = self.v.normalize() * -3000 * dt
            self.v += friction
        else:
            self.v = Vector2(0, 0)
            if self.size > 1:
                self.size -= self.shrink_factor * dt
                self.sprite = py.transform.smoothscale(self.sprite, (int(self.size), int(self.size)))

    def disappearing_animation(self, dt)-> None:
        if self.size > 1:
            self.size -= self.shrink_factor * dt
            self.sprite = py.transform.smoothscale(self.sprite, (int(self.size), int(self.size)))