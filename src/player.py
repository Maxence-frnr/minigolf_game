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

    def draw(self, screen): 
        #py.draw.circle(screen, "white", self.pos, self.radius)
        self.rect = self.sprite.get_rect(center = self.pos)
        screen.blit(self.sprite, self.rect)
        self.particle_group.draw(screen)

    def create_particles(self):
        if self.v.length() > 0:
            Player_Particle(groups=self.particle_group,
                 pos=self.pos,
                 color=(255, 255, 255),
                 direction= -self.v.normalize(),
                 speed=75)
        
    def update_particles(self, dt):
        self.particle_group.update(dt)
        #print(len(self.particle_group.sprites()))