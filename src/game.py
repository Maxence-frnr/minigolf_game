import pygame as py
import math
from pygame import Vector2
from state_manager import BaseState
from utils import Button
from utils import Wall
from utils import Ground
from utils import Wind
from player import Player
from hole import Hole

class Game(BaseState):
    def __init__(self, state_manager, assets_manager, level_manager, sounds_manager):
        #DEBUG
        self.show_ball_speed = False
        self.show_ball_pos = False

        self.state_manager = state_manager
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        self.level_manager = level_manager
        
        self.font = py.font.Font(None, 40)

        
        self.player_sprite = assets_manager.get("ball")
        self.hole_sprite = assets_manager.get("hole")
        self.wind_sprite = assets_manager.get("wind_arrows")
        
        self.swing_sound = sounds_manager.get("swing")
        self.bounce_sound = sounds_manager.get("bounce")
        self.hole_sound = sounds_manager.get("hole")
        
        self.in_game = True
        self.level_to_load = "level_1"
        self.stroke = 0
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
        self.undo_arrow_sprite = assets_manager.get("undo_arrow")
        self.home_sprite = assets_manager.get("home")
        self.next_arrow_sprite = assets_manager.get("next_arrow")
        
        self.back_to_menu_button = Button(text="", rect=py.Rect(30, 30, 30, 30), font_size=10, color=(255, 255, 255), hover_color=(255, 0, 0), action=self.back_to_menu, sprite=self.back_to_menu_button_sprite, sound="click", sounds_manager=sounds_manager)
        self.buttons = [self.back_to_menu_button]
        
        
        #End_level_menu
        self.end_level_menu_elem = []
        self.end_level_menu_elem.append(Button(text="", rect=py.Rect(self.WIDTH//2 + 175, self.HEIGHT//2, 150, 50), font_size=40, color=(255, 255, 255), hover_color=(200, 200, 200), action=self.next_level, sound="click", sounds_manager=sounds_manager, border=True, sprite=self.next_arrow_sprite))
        self.end_level_menu_elem.append(Button(text="", rect=py.Rect(self.WIDTH//2 , self.HEIGHT//2, 150, 50), font_size=40, color=(255, 255, 255), hover_color=(200, 200, 200), action=self.reset, sound="click", sounds_manager=sounds_manager, border=True, sprite=self.undo_arrow_sprite))
        self.end_level_menu_elem.append(Button(text="", rect=py.Rect(self.WIDTH//2- 175, self.HEIGHT//2, 150, 50), font_size=35, color=(255, 255, 255), hover_color=(200, 200, 200), action=self.back_to_menu, sound="click", sounds_manager=sounds_manager, border=True, sprite=self.home_sprite))
        
    def enter(self, **kwargs):
        self.level_to_load = kwargs["level"]
        level = self.level_manager.get_level(self.level_to_load)
        self.player = Player(level["player_pos"], 8, self.player_sprite)
        self.hole = Hole(level["hole_pos"], self.hole_sprite)
        self.walls = []
        if "walls" in level:
            for wall in level["walls"]:
                self.walls.append(Wall((wall["start_pos"]), (wall["end_pos"]), wall["width"], (wall["color"])))
        self.grounds = []
        if "grounds" in level:
            for ground in level["grounds"]:
                self.grounds.append(Ground(py.Rect(ground["rect"]), ground["type"]))
        self.winds = []
        if "winds" in level:
            for wind in level["winds"]:
                self.winds.append(Wind(py.Rect(wind["rect"]), wind["direction"], wind["strength"], self.wind_sprite))
        self.level_to_load = "level_"+self.level_to_load.split("_")[1]
        self.stroke = 0
        self.in_game = True
            
    def next_level(self, *args):
        self.level_to_load = "level_" + str(int(self.level_to_load.split("_")[1]) + 1)
        self.enter(level=self.level_to_load)

    def exit(self):
        self.player.v = Vector2(0, 0)
        self.player.pos = Vector2((self.WIDTH//2, self.HEIGHT//2 + 100))
        self.stroke = 0
        
    def reset(self, *args):
        self.enter(level=self.level_to_load)

    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
    def update(self, dt)->None:
        self.update_player_pos(dt)
        if self.check_win(): self.win() #FIXME: ne pas appeler check_win() a chaque frame
    
    def check_win(self):
        if (self.player.pos - self.hole.pos).length() < 10:          
            return True

    def win(self):
        py.mixer.Sound(self.hole_sound).play()
        print("WIN")
        self.in_game = False
        self.player.v = Vector2(0, 0)
        self.player.pos = Vector2((1100, 1000))
        #self.back_to_menu()
    

    def draw(self, screen):
        #screen.fill((50, 50, 50))
        self.draw_background(screen)
        for ground in self.grounds:
            ground.draw(screen)
        self.hole.draw(screen)
        self.player.draw(screen)
        
        stroke_surface = self.font.render(f"Stroke {self.stroke}", True, (255, 255, 255))
        screen.blit(stroke_surface, py.Rect(self.WIDTH//2 - stroke_surface.get_width()//2, 20, 30, 20))

        for wall in self.walls:
            wall.draw(screen)
            
        for wind in self.winds:
            wind.draw(screen)
        
        #UI
        self.back_to_menu_button.draw(screen)

        if self.builded_strength != Vector2(0, 0):
            self.update_strength_bar(screen)
            screen.blit(self.rotated_image, self.rotated_rect)
        
        if not self.in_game:
            for elem in self.end_level_menu_elem:
                elem.draw(screen)
        if self.show_ball_speed:
            speed = round(self.player.v.length(), 1)
            txt = self.font.render(f"Speed: {speed}", True, (255, 255, 255))
            screen.blit(txt, py.Rect(280, 900, 40, 20))
        
        if self.show_ball_pos:
            pos = self.player.pos
            txt = self.font.render(f"Pos: {pos}", True, (255, 255, 255))
            screen.blit(txt, py.Rect(280, 950, 40, 20))
        
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
        if not self.in_game:
            for elem in self.end_level_menu_elem:
                elem.handle_events(events)
            
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                self.is_left_button_down = True
                
                if abs(event.pos[0] - self.player.pos[0]) < 20 and abs(event.pos[1] - self.player.pos[1]) < 20:
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
                
            keys = py.key.get_pressed()

    def update_player_pos(self, dt): #Calc physics of the player
        if not self.in_game: return
        if self.strength and self.strength.length() > 0:
            self.player.v += self.strength
            self.stroke += 1
            py.mixer.Sound(self.swing_sound).play()
        is_on_special_ground = False
        is_in_wind = False
        if self.player.v.length() > 0:
            for ground in self.grounds:
                if ground.detect_collision(self.player.pos):
                    is_on_special_ground = True
                    self.player.v = ground.handle_collision(self.player.v, dt)
            
            for wind in self.winds:
                if wind.detect_collision(self.player.pos, self.player.radius):
                    is_in_wind = True
                    self.player.v = wind.handle_collision(self.player.v, dt)

        
            if self.player.v.length() > 0 and not is_on_special_ground:
                friction_v = self.player.v.normalize() * -self.friction * dt
                self.player.v += friction_v 

        if self.player.v.length() < 1 and not is_in_wind:
            self.player.v = Vector2(0, 0)

        self.strength = Vector2(0, 0)
        
        #Predict player next pos
        player_next_pos = self.player.pos + self.player.v * dt
        #inverse player velocity if player is out of bounds
        if not (0 <= player_next_pos.x <= self.WIDTH):
            self.player.v.x *= -1
            player_next_pos.x = max(0, min(self.WIDTH, player_next_pos.x))
            py.mixer.Sound(self.bounce_sound).play()

        if not (0 <= player_next_pos.y <= self.HEIGHT):
            self.player.v.y *= -1  
            player_next_pos.y = max(0, min(self.HEIGHT, player_next_pos.y))
            py.mixer.Sound(self.bounce_sound).play()

        #check if the player is in a wall
        for wall in self.walls:
            collision, new_velocity = wall.detect_and_handle_collision(player_next_pos, self.player.radius, self.player.v)
            if collision:
                self.player.v = new_velocity
                player_next_pos = self.player.pos + self.player.v * dt
                py.mixer.Sound(self.bounce_sound).play()

        self.player.pos = player_next_pos
        
    def back_to_menu(self, *args):
        self.state_manager.set_state(name="level_selection_menu")
        
    def build_strength(self, pos):
        direction = -Vector2(pos) + self.player.pos
        self.builded_strength = direction.normalize() * min(direction.length() * self.building_strength_factor, self.max_strength) if direction.length() != 0 else Vector2(0, 0)
        self.strength_arrow_rect = self.calc_strength_arrow_angle(pos)
        
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
        self.rotated_image = py.transform.rotate(self.strength_arrow_sprite, angle + 180)
        self.rotated_rect = self.rotated_image.get_rect(center=self.player.pos)
        #FIXME: clean code
        
    def draw_background(self, screen):
        CELL_SIZE = 50
        screen.fill((131, 177, 73))
        for i in range(self.WIDTH // CELL_SIZE):
            for j in range (self.HEIGHT // CELL_SIZE):
                if (i + j) %2 == 0:
                    py.draw.rect(screen, (161, 197, 75), (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 0 )
                    