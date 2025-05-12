import pygame as py
from state_manager import BaseState
from utils import Button
from utils import Label
import assets_manager

class LevelSelectionMenu(BaseState):
    def __init__(self, state_manager, save_manager, level_manager):
        self.state_manager = state_manager
        self.save_manager = save_manager
        self.level_manager = level_manager
        self.title_font = py.font.Font(None, 50)
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        #création d'un timer pour le retour au menu avec escape pour éviter le double back_to_menu() si le joueur était en partie
        self.can_escape_timer = 45 
        
        go_back_button_sprite = assets_manager.get_image("go_back")
        self.background_sprite = assets_manager.get_image('plain_biome_background')
        self.big_blank_label_sprite = assets_manager.get_image("big_blank_label")
        self.buttons = []
        self.buttons.append(Button(text="", rect=py.Rect(30, 30, 30, 30), font_size=10, color=(255, 255, 255), action=self.back_to_menu, sprite=go_back_button_sprite, sound="click"))
        self.title = Label("Level Selection", py.Rect(self.WIDTH//2, 60, 400, 75), 50, (255, 255, 255))
        self.pos_x = self.WIDTH//2
        self.pos_y = 175
        
        
       
    def create_level_cards(self):
        pos_y = self.pos_y
        unlocked_level_index = self.save_manager.data["level_unlocked"]
        color = (255, 255, 255)
        hover_color = (180, 180, 180)
        level_cards = [[]]
        number_of_level = len(self.level_manager.levels)+1
        for i in range(1, number_of_level):
            level_cards.append([])
            if i > unlocked_level_index:
                color = (200, 70, 70)
                hover_color = (200, 70, 70)
            level_highscore, level_attempts = self.get_level_stats(f"level_{i}")
            level_cards[i].append(Button(rect=py.Rect(self.pos_x, pos_y, 400, 75), action=self.level_selected, action_arg=i, sound="click", sprite=self.big_blank_label_sprite))
            level_cards[i].append(Label(str(i), py.Rect(self.pos_x - 125, pos_y, 50, 50), 65, color, None, True, 3, 10, border_hover_color=(180, 180, 180), hover_rect=py.Rect(self.pos_x - 200, pos_y - 37.5, 400, 75)))
            if level_highscore:
                level_cards[i].append(Label(f"Highscore: {level_highscore}", py.Rect(self.pos_x+50, pos_y-15, 50, 50), 24, color, None))
            if level_attempts:
                level_cards[i].append(Label(f"Attempts: {level_attempts}", py.Rect(self.pos_x+50, pos_y+15, 50, 50), 24, color, None))
            
            pos_y += 125
        
        return level_cards
    
    def get_level_stats(self, level):
        level_highscore = None
        level_attempts = None
        if level in self.save_manager.data["stats"]:
                if "highscore" in self.save_manager.data["stats"][level]:
                    level_highscore = self.save_manager.data["stats"][level]["highscore"]
        else:
            self.save_manager.data["stats"][level] = {}
        if "attempts" in self.save_manager.data["stats"][level]:
            level_attempts = self.save_manager.data["stats"][level]["attempts"]
                    
                    
        return [level_highscore, level_attempts]

    def enter(self, **kwargs):
        self.pos_y = 175
        self.level_cards = self.create_level_cards()
        self.can_escape_timer = 45

    def draw(self, screen):
        screen.blit(self.background_sprite, (0, 0))
        
        self.title.draw(screen)
        
        for button in self.buttons:
            button.draw(screen)
        for card in self.level_cards:
            for i in range(len(card)):
                card[i].draw(screen)
    
    def level_selected(self, index):
        if self.save_manager.data["level_unlocked"] >= index:
            self.state_manager.set_state(name="game", level=f"level_{index}")
    
    def update(self, dt):
        if self.can_escape_timer > 0:
            self.can_escape_timer -= 1
        
    
    def handle_events(self, events:py.event.Event):
        for button in self.buttons:
            button.handle_events(events)
        for card in self.level_cards:
            for i in range(len(card)):
                card[i].handle_events(events)
        for event in events:
            if event.type == py.MOUSEWHEEL:
                self.scroll(event.y)
        
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE] and self.can_escape_timer == 0:
            self.back_to_menu()
    
    def scroll(self, direction):
        scroll_amount = 60
        if direction > 0 and self.level_cards[1][0].rect[1] < 150:
            for card in self.level_cards:
                for elem in card:
                    elem.rect[1] += scroll_amount
                    elem.border_rect[1] += scroll_amount
        elif direction < 0 and self.level_cards[-1][0].rect[1] > 750:
            for card in self.level_cards:
                for elem in card:
                    elem.rect[1] -= scroll_amount
                    elem.border_rect[1] -= scroll_amount
            
    def back_to_menu(self, *args):
        self.state_manager.set_state(name="menu")
    

class LevelCard:
    def __init__(self, pos, index, highscore, function):
        self.font = py.font.Font(None, 20)
        self.pos = pos
        self.index = index
        self.highscore = highscore
        
        self.rect = py.Rect(pos[0], pos[1], 50, 50)
        self.button = Button(str(index), self.rect, 75, (255, 255, 255), (200, 200, 200), function(index))
        self.rect.center = pos
        
    def draw(self, screen):
        self.button.draw(screen)
        py.draw.rect(screen, (200, 100, 200), self.rect, 3, 3)
    
    def handle_events(self, events):
        self.button.handle_events(events)