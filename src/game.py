import pygame as py
import math
import random as r
from pygame import Vector2
from state_manager import BaseState
from utils import Camera, Button, HoleInOneParticule
from obstacles import Wall, Water, Ground, Wind, Blackhole, Portal_entry, Portal_exit
from player import Player
from hole import Hole
import assets_manager

class Game(BaseState):
    def __init__(self, state_manager, level_manager, save_manager):
        #DEBUG
        self.show_ball_speed = False
        self.show_ball_pos = False
        
        self.camera = Camera()

        self.state_manager = state_manager
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        self.level_manager = level_manager
        self.save_manager = save_manager
        
        self.font = py.font.Font(None, 40)

        self.player_sprite = assets_manager.get_image("ball")
        self.hole_sprite = assets_manager.get_image("hole")
        self.wind_sprite = assets_manager.get_image("wind_arrows")
        self.blackhole_sprites = [assets_manager.get_image(f"blackhole{i}" for i in range(1, 10))]
        self.top_ground_sprite = assets_manager.get_image("tree_topground")
        self.background_sprite = assets_manager.get_image("plain_biome_background")
        self.background_detail_sprite = assets_manager.get_image("plain_biome_flowers")
        
        self.swing_sound = assets_manager.get_sound("swing")
        self.bounce_sound = assets_manager.get_sound("bounce")
        self.hole_sound = assets_manager.get_sound("hole")
        self.portal_sound = assets_manager.get_sound("portal")
        
        self.level_to_load = "level_1"
        self.stroke = 0
        self.max_strength = 600.0
        self.strength = None
        self.builded_strength = Vector2(0, 0)
        self.building_strength_factor = 5.0
        self.friction = 200
        self.player_max_speed = 800
        
        self.is_left_button_down = False
        self.is_building_strength = False

        #UI
        self.back_to_menu_button_sprite = assets_manager.get_image("back_arrow")
        self.strength_arrow_sprite = assets_manager.get_image("white_arrow")
        self.undo_arrow_sprite = assets_manager.get_image("undo_arrow")
        self.home_sprite = assets_manager.get_image("home")
        self.next_arrow_sprite = assets_manager.get_image("next_arrow")
        
        self.back_to_menu_button = Button(text="", rect=py.Rect(30, 30, 30, 30), font_size=10, color=(255, 255, 255), hover_color=(255, 0, 0), action=self.back_to_menu, sprite=self.back_to_menu_button_sprite, sound="click")
        self.reset_button = Button(text="", rect=py.Rect(self.WIDTH-30, 30, 150, 50), font_size=10, color=(255, 255, 255), hover_color=(200, 200, 200), action=self.reset, sound="click",  border=False, sprite=self.undo_arrow_sprite)
        self.buttons = [self.back_to_menu_button, self.reset_button]

        self.particle_group = py.sprite.Group()
        self.particle_list = []
        
        
        #End_level_menu
        self.end_level_menu_elem = []
        self.end_level_menu_elem.append(Button(text="", rect=py.Rect(self.WIDTH//2 + 175, 3*self.HEIGHT//5, 150, 50), font_size=40, color=(255, 255, 255), hover_color=(200, 200, 200), action=self.next_level, sound="click", border=True, sprite=self.next_arrow_sprite))
        self.end_level_menu_elem.append(Button(text="", rect=py.Rect(self.WIDTH//2 , 3*self.HEIGHT//5, 150, 50), font_size=40, color=(255, 255, 255), hover_color=(200, 200, 200), action=self.reset, sound="click", border=True, sprite=self.undo_arrow_sprite))
        self.end_level_menu_elem.append(Button(text="", rect=py.Rect(self.WIDTH//2- 175, 3*self.HEIGHT//5, 150, 50), font_size=35, color=(255, 255, 255), hover_color=(200, 200, 200), action=self.back_to_menu, sound="click", border=True, sprite=self.home_sprite))
        
    def enter(self, **kwargs):
        self.is_next_level_available = False
        self.level_to_load = kwargs["level"]
        level = self.level_manager.get_level(self.level_to_load)
        pos = Vector2(level["player_pos"][0]+100, level["player_pos"][1])
        self.player = Player(pos, 8, self.player_sprite)
        pos = Vector2(level["hole_pos"][0]+100, level["hole_pos"][1])
        self.hole = Hole(pos, self.hole_sprite)
        self.walls:list[Wall] = []
        self.waters:list[Water] = []
        self.grounds:list[Ground] = []
        self.winds:list[Wind] = []
        self.blackholes:list[Blackhole] = []
        self.portals_entry:list[Portal_entry] = []
        self.portals_exit:list[Portal_exit] = []
        
        if "walls" in level:
            for wall in level["walls"]:
                rect = py.Rect(wall["rect"][0]+100, wall["rect"][1], wall["rect"][2], wall["rect"][3])
                self.walls.append(Wall(rect, wall["direction"]))
        
        
        if "grounds" in level:
            for ground_type in level["grounds"]:
                for ground in level["grounds"][ground_type]:
                    rect = py.Rect(ground["rect"][0] + 100, ground["rect"][1], ground["rect"][2], ground["rect"][3])
                    if ground_type == "water":
                        self.waters.append(Water(rect, None))
                    else:
                        self.grounds.append(Ground(rect, ground_type))
        
        if "winds" in level:
            for wind in level["winds"]:
                rect = py.Rect(wind["rect"][0] + 100, wind["rect"][1], wind["rect"][2], wind["rect"][3])
                self.winds.append(Wind(rect, wind["direction"], wind["strength"], self.wind_sprite))
        
        if "blackholes" in level:
            for blackhole in level["blackholes"]:
                pos = Vector2(blackhole["pos"][0] + 100, blackhole["pos"][1])
                self.blackholes.append(Blackhole(pos, blackhole["radius"], blackhole["strength"], self.blackhole_sprites))
        
        if "portals" in level:
            for portals in level["portals"]:
                entry_pos = Vector2(portals["entry_pos"][0] + 100, portals["entry_pos"][1])
                exit_pos = Vector2(portals["exit_pos"][0] + 100, portals["exit_pos"][1])
                self.portals_entry.append(Portal_entry(entry_pos, exit_pos))
                self.portals_exit.append(Portal_exit(exit_pos))
                
        self.level_to_load = "level_"+self.level_to_load.split("_")[1]
        if "attempts" in self.save_manager.data["stats"][self.level_to_load]:
            self.save_manager.data["stats"][self.level_to_load]["attempts"] += 1
        else:
            self.save_manager.data["stats"][self.level_to_load] = {}
            self.save_manager.data["stats"][self.level_to_load]["attempts"] = 1
        self.stroke = 0
        self.in_game = True

            
    def next_level(self, *args):    
        self.level_to_load = "level_" + str(int(self.level_to_load.split("_")[1]) + 1)
        if self.level_manager.get_level(self.level_to_load) != None:
            self.enter(level=self.level_to_load)
        else:
            self.back_to_menu()
        
    def reset(self, *args):
        self.enter(level=self.level_to_load)

    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
    def update(self, dt)->None:
        if (self.player.drowning  or self.player.disappearing) and self.player.size <= 1 and self.in_game:
            self.game_over()
        self.update_player_pos(dt)
        self.camera.update()
        
        self.player.update(dt)

        for water in self.waters:
            water.update(dt)

        for blackhole in self.blackholes:
            blackhole.update(dt)

        for wind in self.winds:
            wind.update(dt)
        
        for portal_entry in self.portals_entry:
            portal_entry.update(dt)
        for portal_exit in self.portals_exit:
            portal_exit.update(dt)
        
        self.particle_group.update(dt)

    def win(self):
        self.is_next_level_available = True
        py.mixer.Sound(self.hole_sound).play()
        print("called game over")
        self.save_progression()
        self.in_game = False
        
        #self.back_to_menu()
        if self.stroke == 1:
            for i in range(12):
                alpha = i * math.pi/6
                self.particle_list.append(HoleInOneParticule(self.particle_group, Vector2(self.hole.pos.x + 20 * math.cos(alpha), self.hole.pos.y + 20 * math.sin(alpha)), (255, 20, 80), Vector2(500 * math.cos(alpha), 500 * math.sin(alpha)), 12))
        
    def game_over(self):
        self.in_game = False
    
    def save_progression(self):
        if "highscore" in self.save_manager.data["stats"][str(self.level_to_load)] and self.stroke < self.save_manager.data["stats"][str(self.level_to_load)]["highscore"]:
            self.save_manager.data["stats"][str(self.level_to_load)]["highscore"] = self.stroke
        else:
            self.save_manager.data["stats"][str(self.level_to_load)]["highscore"] = self.stroke
        if int(self.level_to_load.split("_")[1])+1 > self.save_manager.data["level_unlocked"]:
            self.save_manager.data["level_unlocked"] = int(self.level_to_load.split("_")[1])+1
        self.save_manager.save_data()
    
    def draw(self, screen):
        #screen.fill((50, 50, 50))
        offset = self.camera.offset
        self.draw_background(screen, offset)
        py.draw.line(screen, (0, 0, 0), (100, 0), (100, 1000), 2)
        py.draw.line(screen, (0, 0, 0), (700, 0), (700, 1000), 2)
        for blackhole in self.blackholes:
            blackhole.draw(screen)
        for water in self.waters:
            water.draw(screen, offset)
        for ground in self.grounds:
            ground.draw(screen)
        self.hole.draw(screen, offset)
        if self.in_game:
            self.player.draw(screen, offset)
        
        for portal in self.portals_entry:
            portal.draw(screen, offset)
        for portal in self.portals_exit:
            portal.draw(screen, offset)
        
        for blackhole in self.blackholes:
            blackhole.draw(screen)

        for wall in self.walls:
            wall.draw(screen, self.camera.offset)
        
        for wind in self.winds:
            wind.draw(screen)
                  
        stroke_surface = self.font.render(f"Stroke {self.stroke}", True, (255, 255, 255))
        screen.blit(stroke_surface, py.Rect(self.WIDTH//2 - stroke_surface.get_width()//2, 20, 30, 20))
        
        rect = py.Rect(offset.x, offset.y, self.WIDTH, self.HEIGHT)
        screen.blit(self.top_ground_sprite, rect)
        
        
        #UI
        if self.in_game:
            for button in self.buttons:
                button.draw(screen)

        if self.builded_strength != Vector2(0, 0):
            self.update_strength_bar(screen)
            screen.blit(self.rotated_image, self.rotated_rect)
        
        if not self.in_game:
            for elem in self.end_level_menu_elem:
                if self.is_next_level_available == False and elem.action == self.next_level:
                    continue
                elem.draw(screen)
        if self.show_ball_speed:
            speed = round(self.player.v.length(), 1)
            txt = self.font.render(f"Speed: {speed}", True, (255, 255, 255))
            screen.blit(txt, py.Rect(280, 900, 40, 20))
        
        if self.show_ball_pos:
            pos = self.player.pos
            txt = self.font.render(f"Pos: {pos}", True, (255, 255, 255))
            screen.blit(txt, py.Rect(280, 950, 40, 20))
        
        self.particle_group.draw(screen)
        
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
        if not self.in_game:
            for elem in self.end_level_menu_elem:
                if self.is_next_level_available == False and elem.action == self.next_level:
                    continue
                elem.handle_events(events)
            
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN and self.in_game:
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
            if keys[py.K_SPACE]:
                self.camera.start_shake(5)
            if keys[py.K_r] and self.stroke > 0:
                self.reset()
                self.camera.start_shake(0.7)
            if keys[py.K_ESCAPE]:
                self.back_to_menu()
            
            if keys[py.K_e]:
                mp = py.mouse.get_pos()
                print("mp", mp)

    def update_player_pos(self, dt): #Calc physics of the player
        if not self.in_game: return
        if self.strength and self.strength.length() > 0:
            self.player.v += self.strength
            self.stroke += 1
            py.mixer.Sound(self.swing_sound).play()
        is_on_special_ground = False
        is_in_wind = False
        is_in_blackhole = False
        if self.player.v.length() > 0:
            for ground in self.grounds:
                if ground.detect_collision(self.player.pos):
                    is_on_special_ground = True
                    self.player.v = ground.handle_collision(self.player.v, dt)
                
            for water in self.waters:
                if water.detect_collision(self.player.pos, self.player.radius):
                    self.player.v = water.handle_collision(self.player.v, dt)
                    if self.player.v.length() < 50:
                        if self.player.size <= 1:
                            self.game_over()
                        self.player.drowning = True

            
            if self.hole.detect_collision(self.player.pos, self.player.radius):
                self.win()
            
            for wind in self.winds:
                if wind.detect_collision(self.player.pos, self.player.radius):
                    is_in_wind = True
                    self.player.v = wind.handle_collision(self.player.v, dt)
            
            for blackhole in self.blackholes:
                if blackhole.detect_collision(self.player.pos, self.player.radius):
                    is_in_blackhole = True
                    self.player.v = blackhole.handle_collision(self.player.pos, self.player.v, dt)
                    radius = blackhole.radius
                    d = blackhole.pos.distance_to(self.player.pos)
                    #print(self.player.v.length(), math.exp(-5* (d / radius)) * 1000)
                    if self.player.v.length() <= math.exp(-5* (d / radius)) * 1000:
                        self.player.disappearing = True
                    
            for portal in self.portals_entry:    
                if portal.detect_collision(self.player.pos, self.player.radius):
                    self.player.pos = portal.handle_collision()
                    py.mixer.Sound(self.portal_sound).play()

        
            if self.player.v.length() > 0 and not is_on_special_ground:
                friction_v = self.player.v.normalize() * -self.friction * dt
                self.player.v += friction_v 
                
            
        #Stop the player if speed is near zero
        #Only if the player isn't in a wind or blackhole
        if self.player.v.length() < 1 and not is_in_wind and not is_in_blackhole: 
            self.player.v = Vector2(0, 0)
        
        #Cap the player speed
        if self.player.v.length() > self.player_max_speed:
            self.player.v = self.player.v.normalize() * self.player_max_speed

        self.strength = Vector2(0, 0)
        
        #Predict player next pos
        player_next_pos = self.player.pos + self.player.v * dt
        #inverse player velocity if player is out of bounds
        if not (100 + self.player.radius <= player_next_pos.x <= self.WIDTH-100 - self.player.radius):
            self.player.v.x *= -1
            player_next_pos.x = max(0, min(self.WIDTH, player_next_pos.x))
            py.mixer.Sound(self.bounce_sound).play()
            self.camera.start_shake(self.player.v.length()/250)

        if not (self.player.radius <= player_next_pos.y <= self.HEIGHT - self.player.radius):
            self.player.v.y *= -1  
            player_next_pos.y = max(0, min(self.HEIGHT, player_next_pos.y))
            py.mixer.Sound(self.bounce_sound).play()
            self.camera.start_shake(self.player.v.length()/250)

        #check if the player is in a wall
        for wall in self.walls:
            if wall.detect_collision(player_next_pos, self.player.radius):
                self.player.v = wall.handle_collision(self.player.v, player_next_pos, self.player.radius)
                player_next_pos = self.player.pos + self.player.v * dt
                py.mixer.Sound(self.bounce_sound).play()
                self.camera.start_shake(self.player.v.length()/250)

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
        
    def draw_background(self, screen:py.Surface, offset:Vector2 = Vector2(0, 0)):
        rect = py.Rect(offset.x, offset.y, self.WIDTH, self.HEIGHT)
        screen.blit(self.background_sprite, rect)
        screen.blit(self.background_detail_sprite, rect)
        # CELL_SIZE = 50
        # screen.fill((131, 177, 73))
        # for i in range(self.WIDTH // CELL_SIZE):
        #     for j in range (self.HEIGHT // CELL_SIZE):
        #         if (i + j) %2 == 0:
        #             py.draw.rect(screen, (161, 197, 75), (i*CELL_SIZE + offset[0], j*CELL_SIZE+offset[1], CELL_SIZE, CELL_SIZE), 0 )
                    