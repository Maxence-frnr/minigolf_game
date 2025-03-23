import pygame as py
import math
from pygame import Vector2

py.init()

screen = py.display.set_mode((400, 400))
clock = py.time.Clock()



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
        py.draw.circle(screen, "blue", self.corners[0], 2)
        py.draw.circle(screen, "orange", self.corners[1], 2)
        py.draw.circle(screen, "green", self.corners[2], 2)
        py.draw.circle(screen, "cyan", self.corners[3], 2)
        
    def detect_collision(self, player_pos, player_radius):
        return self.sat_collision(player_pos, player_radius)
    
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

class Player:
    def __init__(self, pos:py.Vector2, radius):
        self.radius = radius
        self.pos = pos
        self.v = py.Vector2(-2, -10)

    def draw(self, screen): 
        py.draw.circle(screen, "purple", self.pos, self.radius)
    
    def update(self):
        self.pos += self.v

    
###
wall = Wall2(py.Rect(200, 100, 100, 50), 30)
wall2 = Wall2(py.Rect(300, 300, 100, 50), -30)
ball = Player(Vector2(200, 300), 10)

running = True
while running:
    dt = clock.tick(60) / 1000
    clock.tick(50)
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
    screen.fill((255, 255, 255))
    
    #######
    if not (0+ ball.radius < ball.pos.x < 400 - ball.radius):
        ball.v.x *= -1
    if not (0 + ball.radius< ball.pos.y < 400- ball.radius):
        ball.v.y *= -1
    wall.draw(screen)
    wall2.draw(screen)
    ball.draw(screen)
    
    next_pos = ball.pos + ball.v
    if wall.detect_collision(next_pos, ball.radius):
        ball.v = wall.handle_collision(ball.v, next_pos, ball.radius)
    if wall2.detect_collision(next_pos, ball.radius):
        ball.v = wall2.handle_collision(ball.v, next_pos, ball.radius)
    ball.update()

    

    
    
    #######
    py.display.update()
py.quit()
#TODO: Cry