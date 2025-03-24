import pygame as py
from utils import Player_Particle

class Player:
    def __init__(self, pos:py.Vector2, radius, sprite, particle_sprite):
        self.radius = radius
        self.pos = pos
        self.v = py.Vector2(0, 0)
        self.sprite = sprite
        self.particle_sprite = particle_sprite
        self.rect = self.sprite.get_rect(center = self.pos)
        self.particle_group = py.sprite.Group()
        
        self.particle_timer = 0
        self.base_interval = 0.2 #en secondes

    def draw(self, screen, offset:py.Vector2 = py.Vector2(0, 0)): 
        #py.draw.circle(screen, "white", self.pos, self.radius)
        self.rect = self.sprite.get_rect(center = self.pos+ offset)
        screen.blit(self.sprite, self.rect)
        self.particle_group.draw(screen)

    def create_particles(self):
        if self.v.length() > 0:
            Player_Particle(groups=self.particle_group,
                 pos=self.pos,
                 color=(255, 255, 255),
                 direction= -self.v.normalize(),
                 speed= self.v.length()/2)
        
    def update_particles(self, dt):
        pass
        #print(len(self.particle_group.sprites()))
    
    def update(self, dt:float)-> None:
        self.particle_group.update(dt)
        
        speed = self.v.length()
        scaled_interval = max(self.base_interval / (speed / 300 + 1), 0.07)
        
        self.particle_timer -= dt
        if self.particle_timer <= 0:
            self.create_particles()
            self.particle_timer = scaled_interval
        