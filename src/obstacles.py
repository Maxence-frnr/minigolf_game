import pygame as py
from pygame import Vector2
import math


class Wall:
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

    
    def draw(self, screen, offset:Vector2= Vector2(0, 0)):
        shaken_corners = [corner + offset for corner in self.corners]
        py.draw.polygon(screen, (255, 0, 0), shaken_corners, 2)
        
    def detect_collision(self, player_pos, player_radius):
        return self.sat_collision(player_pos, player_radius)
    
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

    def orthogonal_projection(self, P:Vector2, A:Vector2, B:Vector2):
        #Projette le point P sur le segment A, B
        #Plus permissif que la fonction project_polygone
        segment = B - A
        segment_length_squared = segment.dot(segment)
        if segment_length_squared == 0:
            return None
        projection = A + segment.dot((P- A)) / segment.dot(segment) * segment
        t = segment.dot((P - A)) / segment.dot(segment)
        if 0 <= t <= 1:
            return projection
        return None        
    
    def detect_collision_face(self, P:Vector2, r:float, corners:list[Vector2]):
        faces = [("AB", corners[0], corners[1]),
                 ("BC", corners[1], corners[2]),
                 ("CD", corners[2], corners[3]),
                 ("DA", corners[3], corners[0])]
        
        closest_face = None
        min_distance = float('inf')
        #check quelle face est la plus proche du joueur en projetant le joueur sur chacune des faces
        for name, S1, S2 in faces:
            P_proj = self.orthogonal_projection(P, S1, S2)
            if P_proj is not None:
                d = P.distance_to(P_proj)
                if d <= r and d < min_distance:
                    min_distance = d
                    closest_face = (name, S1, S2)
                    
        
        closest_vertex = None
        min_vertex_distance = float('inf')
        #check quelle sommet est le plus proche du joueur
        for i, vertex in enumerate(corners):
            d = P.distance_to(vertex)
            if d <= r and d < min_vertex_distance:
                min_vertex_distance = d
                closest_vertex = vertex
        
        if closest_vertex and (closest_vertex is None or min_vertex_distance < min_distance):
            #Si un vertex est plus proche qu'une des face on le retourne à la place
            return ("Vertex", closest_vertex, None)
        
        return closest_face
        
    def handle_collision(self, player_velocity:Vector2, player_pos:Vector2, player_radius:float):
        f = self.detect_collision_face(player_pos, player_radius, self.corners)

        if f is None:
            return player_velocity
        
        if f[0] == "Vertex":
            normal = (player_pos - f[1]).normalize()
        else:
            normal = Vector2(-(f[2].y - f[1].y), (f[2].x - f[1].x)).normalize()

            if normal.dot(player_velocity) > 0:
                normal = -normal  # Flip the normal
        print(normal)
        return player_velocity - 2*(player_velocity.dot(normal)) * normal
     
    
class Water:
    def __init__(self, rect:py.Rect, sprite=None):
        self.rect = rect
        self.friction = 1000
        self.sprite = sprite
        self.rect.center = (rect[0], rect[1])
        
    def draw(self, screen, offset:Vector2=Vector2(0, 0)):
        py.draw.rect(screen, (50, 50, 200), self.rect)
    
    def detect_collision(self, player_pos:Vector2, player_radius:float)->bool:
        return self.rect.collidepoint(player_pos)
    
    def handle_collision(self, player_velocity:Vector2, dt:float)->Vector2:
        friction_v = player_velocity.normalize() * -self.friction * dt
        player_velocity += friction_v
        return player_velocity
      
    
class Ground:
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
    
    
class Wind:
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
    def __init__(self, pos, radius, strength, sprites:list[py.sprite.Sprite]):
        self.pos = Vector2(pos)
        self.radius = radius
        self.strength = strength
        self.sprites = []
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x1.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x2.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x3.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x4.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x5.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x6.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x7.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x8.png"))
        self.sprites.append(py.image.load("assets\\sprites\\blackhole_anim_256x9.png"))
        for i in range(len(self.sprites)):
            self.sprites[i] = py.transform.scale(self.sprites[i], (radius*2, radius*2))
        self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.sprite_index += 0.2
        if self.sprite_index > len(self.sprites) -1 :
            self.sprite_index = 0
        self.image = self.sprites[int(self.sprite_index)]
    
    def draw(self, screen:py.Surface):
        #py.draw.circle(screen, (255, 10, 15), self.pos, self.radius, 5)
        screen.blit(self.image, self.rect)
    
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
    
    def draw(self, screen, offset:Vector2= Vector2(0, 0)):
        py.draw.circle(screen, (0, 150, 210), self.pos + offset, self.radius, 5)
        
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
    
    def draw(self, screen, offset:Vector2= Vector2(0, 0)):
        py.draw.circle(screen, (230, 130, 10), self.pos + offset, self.radius, 5)
        
        
