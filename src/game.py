import pygame as py
import math
from pygame import Vector2
from state_manager import BaseState
from utils import Button
from utils import Wall
from player import Player
from hole import Hole

class Game(BaseState):
    def __init__(self, state_manager, assets_manager):
        self.state_manager = state_manager
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        self.player = Player((self.WIDTH//2, self.HEIGHT//2 + 100), 7)

        self.font = py.font.Font(None, 40)

        self.stroke = 0

        hole_sprite = assets_manager.get("hole")
        self.hole = Hole((self.WIDTH//2, 200), hole_sprite)

        self.max_strength = 600.0
        self.strength = None
        self.builded_strength = Vector2(0, 0)
        self.building_strength_factor = 5.0
        self.friction = 200
        
        self.is_left_button_down = False
        self.is_building_strength = False
        
        self.strength_arrow_angle = 0

        
        #UI
        self.back_to_menu_button_sprite = assets_manager.get("back_arrow")
        self.strength_arrow_sprite = assets_manager.get("white_arrow")
        
        self.back_to_menu_button = Button("", (10, 10, 30, 30), 10, (255, 255, 255), (255, 0, 0), self.back_to_menu, self.back_to_menu_button_sprite)
        self.buttons = [self.back_to_menu_button]

        #Level1 FIXME: à deplacer dans level.json et y charger 

        self.walls = []
        self.walls.append(Wall((100, self.HEIGHT - 50),(500, self.HEIGHT-50), 19, (170, 170 ,245)))#horizontale bas
        self.walls.append(Wall((109, self.HEIGHT - 60),(109, 70), 19, (170, 170 ,245)))#vertical gauche
        self.walls.append(Wall((100, 60),(500, 60), 19, (170, 170 ,245)))#horizontal haut
        self.walls.append(Wall((491, 70),(491, self.HEIGHT-60), 19, (170, 170 ,245)))#vertical droite


    
    def enter(self):
        pass
    
    def exit(self):
        self.player.v = Vector2(0, 0)
        self.player.pos = Vector2((self.WIDTH//2, self.HEIGHT//2 + 100))
        self.stroke = 0

    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
    def update(self, dt)->None:
        self.update_player_pos(dt)
        if self.check_win(): self.win() #FIXME: ne pas appeler check_win() a chaque frame
    
    def check_win(self):
        if (self.player.pos - self.hole.pos).length() < 10:          
            return True

    def win(self):
        print("WIN")
        self.back_to_menu()

    def draw(self, screen):
        screen.fill((50, 50, 50))
        self.hole.draw(screen)
        self.player.draw(screen)
        stroke_surface = self.font.render(f"Stroke {self.stroke}", True, (255, 255, 255))
        screen.blit(stroke_surface, py.Rect(self.WIDTH//2 - stroke_surface.get_width()//2, 20, 30, 20))

        for wall in self.walls:
            wall.draw(screen)
        
        #UI
        self.back_to_menu_button.draw(screen)

        if self.builded_strength != Vector2(0, 0):
            self.update_strength_bar(screen)
            screen.blit(self.rotated_image, self.rotated_rect)
        
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                self.is_left_button_down = True
                
                if abs(event.pos[0] - self.player.pos[0]) < 15 and abs(event.pos[1] - self.player.pos[1]) < 15:
                    self.is_building_strength = True
                    
            elif event.type == py.MOUSEBUTTONUP:
                self.is_left_button_down = False
                self.is_building_strength = False
                if self.builded_strength.length() > 0:
                    self.strength = self.builded_strength
                self.builded_strength = Vector2(0, 0)
                
            elif event.type == py.MOUSEMOTION:
                if self.is_left_button_down and self.is_building_strength:
                    self.build_strength(event.pos)
                    
    
    def update_player_pos(self, dt): #Calc physics of the player
        if self.strength and self.strength.length() > 0:
            self.player.v += self.strength
            self.stroke += 1

        if self.player.v.length() > 0:
            friction_v = self.player.v.normalize() * -self.friction * dt
            self.player.v += friction_v 

            if self.player.v.length() < 1:
                self.player.v = Vector2(0, 0)

        self.strength = Vector2(0, 0)
        
        #Predict player next pos
        player_next_pos = self.player.pos + self.player.v * dt
        #inverse player velocity if player is out of bounds
        if not (0 <= player_next_pos.x <= self.WIDTH):
            self.player.v.x *= -1
            player_next_pos.x = max(0, min(self.WIDTH, player_next_pos.x))

        if not (0 <= player_next_pos.y <= self.HEIGHT):
            self.player.v.y *= -1     
            player_next_pos.y = max(0, min(self.HEIGHT, player_next_pos.y))

        #check if the player is in a wall
        for wall in self.walls:
            collision, new_velocity = wall.detect_and_handle_collision(player_next_pos, self.player.radius, self.player.v)
            if collision:
                self.player.v = new_velocity
                player_next_pos = self.player.pos + self.player.v * dt

        self.player.pos = player_next_pos
        
    def back_to_menu(self):
        self.state_manager.set_state("menu")
        
    def build_strength(self, pos):
        direction = -Vector2(pos) + self.player.pos
        self.builded_strength = direction.normalize() * min(direction.length() * self.building_strength_factor, self.max_strength) if direction.length() != 0 else Vector2(0, 0)
        self.strength_arrow_rect = self.calc_strength_arrow_angle(pos)
        #print(self.builded_strength)
        
    def update_strength_bar(self, screen):
        builded_strength_length = self.builded_strength.length()
        builded_strength_bar = (self.player.pos[0] + 20, self.player.pos[1] + 5 -abs(builded_strength_length/20) , 7, abs(builded_strength_length/20))
        max_builded_strength_bar = (self.player.pos[0] + 20 - 1, self.player.pos[1] + 5 - 600/20-2, 9, 600/20+4)

        red_value = min(builded_strength_length // (self.max_strength/510), 255)
        green_value = min(510 - builded_strength_length // (self.max_strength/510), 255)
        color = (red_value, green_value, 0)
        py.draw.rect(screen, (150, 155, 155), max_builded_strength_bar)
        py.draw.rect(screen, color, builded_strength_bar)
    
    def calc_strength_arrow_angle(self, pos):
        direction:Vector2 = pos - self.player.pos
        angle = direction.angle_to(Vector2(1, 0))
        if angle < 0:
            angle = 360 + angle
        #print(angle)
        self.rotated_image = py.transform.rotate(self.strength_arrow_sprite, angle + 180)
        self.rotated_rect = self.rotated_image.get_rect(center=self.player.pos)
        #FIXME: clean code