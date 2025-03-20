import pygame as py
import math
import random as r
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
                self.is_hovered = py.Rect.collidepoint(self.border_rect, event.pos)
            elif event.type == py.MOUSEBUTTONDOWN and self.is_hovered and py.mouse.get_pressed()[0]:
                self.action(self.action_arg)
                if self.sounds_manager:
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
            py.draw.rect(screen, color, self.border_rect, 3, 3)
        if self.sprite: screen.blit(self.sprite, self.sprite_rect)
        text = self.font.render(self.text, True, color)
        text_rect = text.get_rect(center= (self.rect[0], self.rect[1]))
        screen.blit(text, text_rect)
    
    def handle_events(self, events:py.event.Event):
        pass

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
    
class Wall2():
    def __init__(self, rect:py.Rect, direction:int):
        self.direction = Vector2(round(math.cos(math.radians(direction)), 2), 
                                 -round(math.sin(math.radians(direction)), 2))
        self.angle = direction

        self.center  = (rect[0], rect[1])
        self.width = rect[2]
        self.height = rect[3]
        
        self.update_corners()
        
    def update_corners(self):
        half_width, half_height = self.width//2, self.height //2
        rad = math.radians(-self.angle)
        corners = [Vector2(-half_width, -half_height),
                   Vector2(half_width, -half_height),
                   Vector2(half_width, half_height),
                   Vector2(-half_width, half_height)]
        
        self.corners = [self.center + point.rotate_rad(rad) for point in corners]

    
    def draw(self, screen):
        py.draw.polygon(screen, (255, 0, 0), self.corners, 2)
        
    def detect_collision(self, player_pos, player_radius):
        return self.sat_collision(player_pos, player_radius)
    
    def handle_collision(self, player_velocity:Vector2, dt):
        return -player_velocity
    
    #TODO: relire le code
    def project_polygon(self, axis, points):
        """ Projette un polygone sur un axe donné et retourne le min et max """
        dots = [point.dot(axis) for point in points]
        return min(dots), max(dots)

    def sat_collision(self, player_pos, player_radius):
        """ Implémente le théorème de séparation des axes (SAT) pour la collision rectangle-cercle """
        # Ajouter le cercle comme un point + rayon
        circle_center = Vector2(player_pos)

        # Liste des axes de séparation (normales des bords du rectangle)
        axes = []
        for i in range(len(self.corners)):
            edge = self.corners[i] - self.corners[(i + 1) % len(self.corners)]
            normal = Vector2(-edge.y, edge.x).normalize()
            axes.append(normal)

        # Ajouter un axe passant par le centre du cercle et le point le plus proche
        closest_point = min(self.corners, key=lambda p: (p - circle_center).length_squared())
        axes.append((closest_point - circle_center).normalize())

        # Vérification des projections sur chaque axe
        for axis in axes:
            min_rect, max_rect = self.project_polygon(axis, self.corners)
            min_circle = circle_center.dot(axis) - player_radius
            max_circle = circle_center.dot(axis) + player_radius

            # Si les projections ne se chevauchent pas, il n'y a pas de collision
            if max_circle < min_rect or min_circle > max_rect:
                return False

        # Si toutes les projections se chevauchent, il y a une collision
        return True


class Ground():
    def __init__(self, rect:py.Rect, type):
        self.rect = rect
        if type == "sand":
            self.color = (255, 207, 92)
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
    
class Wind():
    def __init__(self, rect:py.Rect, direction:int, strength:int, sprite):
        self.direction = Vector2(round(math.cos(math.radians(direction)), 2), 
                                 -round(math.sin(math.radians(direction)), 2))
        self.strength = self.direction * strength
        self.angle = direction
        
        self.sprite = py.transform.scale(sprite, (rect[2], rect[3]))
        self.sprite = py.transform.rotate(self.sprite, direction)

        self.center  = (rect[0], rect[1])
        self.width = rect[2]
        self.height = rect[3]
        
        self.update_corners()
        
    def update_corners(self):
        half_width, half_height = self.width//2, self.height //2
        rad = math.radians(-self.angle)
        corners = [Vector2(-half_width, -half_height),
                   Vector2(half_width, -half_height),
                   Vector2(half_width, half_height),
                   Vector2(-half_width, half_height)]
        
        self.corners = [self.center + point.rotate_rad(rad) for point in corners]

    
    def draw(self, screen):
        screen.blit(self.sprite, self.sprite.get_rect(center = self.center))
        #py.draw.polygon(screen, (255, 0, 0), self.corners, 2)
        
    def detect_collision(self, player_pos, player_radius):
        return self.sat_collision(player_pos, player_radius)
    
    def handle_collision(self, player_velocity:Vector2, dt):
        return player_velocity + self.strength * dt
    
    #TODO: relire le code
    def project_polygon(self, axis, points):
        """ Projette un polygone sur un axe donné et retourne le min et max """
        dots = [point.dot(axis) for point in points]
        return min(dots), max(dots)

    def sat_collision(self, player_pos, player_radius):
        """ Implémente le théorème de séparation des axes (SAT) pour la collision rectangle-cercle """
        # Ajouter le cercle comme un point + rayon
        circle_center = Vector2(player_pos)

        # Liste des axes de séparation (normales des bords du rectangle)
        axes = []
        for i in range(len(self.corners)):
            edge = self.corners[i] - self.corners[(i + 1) % len(self.corners)]
            normal = Vector2(-edge.y, edge.x).normalize()
            axes.append(normal)

        # Ajouter un axe passant par le centre du cercle et le point le plus proche
        closest_point = min(self.corners, key=lambda p: (p - circle_center).length_squared())
        axes.append((closest_point - circle_center).normalize())

        # Vérification des projections sur chaque axe
        for axis in axes:
            min_rect, max_rect = self.project_polygon(axis, self.corners)
            min_circle = circle_center.dot(axis) - player_radius
            max_circle = circle_center.dot(axis) + player_radius

            # Si les projections ne se chevauchent pas, il n'y a pas de collision
            if max_circle < min_rect or min_circle > max_rect:
                return False

        # Si toutes les projections se chevauchent, il y a une collision
        return True
    
class Blackhole:
    def __init__(self, pos, radius, strength, sprite):
        self.pos = Vector2(pos)
        self.radius = radius
        self.strength = strength
        self.sprite = sprite
    
    def draw(self, screen):
        py.draw.circle(screen, (10, 10, 15), self.pos, self.radius, 5)
    
    def detect_collision(self, player_pos:Vector2, player_radius):
        d = self.pos.distance_to(player_pos)
        return d < self.radius + player_radius

    
    def handle_collision(self, player_pos:Vector2, player_v:Vector2, dt):
        r = self.pos - player_pos
        d = r.length()
        if d == 0:
            return player_v
        
        norme_f = 500* self.strength / (d)
        f = r.normalize() * norme_f
        return player_v + f * dt
    
class Portal_entry:
    def __init__(self, pos:Vector2, exit_pos:Vector2, sprite:py.image=None):
        self.pos = pos
        self.radius = 20
        self.exit_pos = exit_pos
        self.sprite = sprite
    
    def draw(self, screen):
        py.draw.circle(screen, (0, 150, 210), self.pos, self.radius, 5)
        
    def detect_collision(self, player_pos:Vector2, player_radius:float):
        d = self.pos.distance_to(player_pos)
        return d < self.radius + player_radius
    
    def handle_collision(self):
        return self.exit_pos
    
class Portal_exit:
    def __init__(self, pos:Vector2, sprite:py.image=None):
        self.pos = pos
        self.sprite = sprite
        self.radius = 20
    
    def draw(self, screen):
        py.draw.circle(screen, (230, 130, 10), self.pos, self.radius, 5)
        
class Particle(py.sprite.Sprite):
    def __init__(self, 
                groups: py.sprite.Group, 
                pos: Vector2, 
                color: tuple, 
                direction: Vector2, 
                speed: float,
                size:int,
                sprite: py.image=None):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
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
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.move(dt)

class Player_Particle(Particle):
    def __init__(self, 
                 groups:py.sprite.Group, 
                 pos, 
                 color, 
                 direction, 
                 speed,
                 sprite:py.image = None):
        k1 = r.uniform(-0.4, 0.4)
        k2 = k1 = r.uniform(-0.4, 0.4)
        direction = py.Vector2(direction[0] +k1 , direction[1] + k2).normalize()
        size = r.randint(2, 8)
        
        super().__init__(groups, pos, color, direction, speed, size, sprite)
        
        self.scale = 1
        self.alpha = 255
        self.angle = r.randint(0, 359)

        self.inflate_speed = 5
        self.fade_speed = 400
        self.rotation_speed = round(r.uniform(-1, 1))
        self.slowing_speed = 75

        self.max_size = 20
        self.min_speed = 1
        #self.image = py.transform.rotate(self.image, self.angle)
        #self.rect = self.image.get_rect(center=self.pos)
        #self.size = self.sprite.get_width()

    def slow(self, dt):
        if self.speed > self.min_speed:
            self.speed -= self.slowing_speed * dt


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