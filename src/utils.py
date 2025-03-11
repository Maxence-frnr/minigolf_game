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
                self.is_hovered = py.Rect.collidepoint(self.border_rect, event.pos)
            elif event.type == py.MOUSEBUTTONDOWN and self.is_hovered:
                if self.text == "Next":
                    print(self.action_arg)
                self.action(self.action_arg)
                if self.sounds_manager:
                    py.mixer.Sound(self.sound).play()
    
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
        print("r: ", r)
        print("f", f)
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
        
