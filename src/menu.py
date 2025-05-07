import pygame as py
from state_manager import BaseState
from utils import Button, Label
import assets_manager, state_manager

class MenuState(BaseState):
    def __init__(self, state_manager, save_manager):
        self.state_manager = state_manager
        #UI elements to enable
        self.title_font = py.font.Font(None, 125)
        
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
        
        self.play_button = Button("Play", py.Rect(self.WIDTH//2, self.HEIGHT//2, 130, 80), 75, (255, 255, 255), (210, 210, 210), self.play, border=True, sound="click")
        self.exit_button = Button("Exit", py.Rect(self.WIDTH//2, 700, 100, 70), 60, (255, 255, 255), (210, 210, 210), self.exit_game, border=True)
        self.buttons = [self.play_button, self.exit_button]
        self.background_music = assets_manager.get_sound("background_music")
        self.save_manager = save_manager

        self.saved_volume = save_manager.data["music_volume"]

        self.volume_label = Label(str(int(self.saved_volume* 100)), py.Rect(400, 600, 50, 30), border= True, border_width=2)
        self.volume_plus_button = Button('+', py.Rect(450, 600, 25, 25), border= True, border_width=2, action=self.update_volume, action_arg=0.1, sound='click')
        self.volume_minus_button = Button('-', py.Rect(350, 600, 25, 25), border= True, border_width=2, action=self.update_volume, action_arg=-0.1, sound='click')

        self.buttons.append(self.volume_plus_button)
        self.buttons.append(self.volume_minus_button)

        
    def update_window_size(self, screen):
        self.WIDTH, self.HEIGHT = py.display.get_window_size()
    
    def update_volume(self, change)->None:
        current_volume = py.mixer.music.get_volume()
        if current_volume + change < 0:
            new_volume = 0.0
        elif current_volume + change > 1.0:
            new_volume = 1.0
        else:
            new_volume = int(5 * round(float(int((current_volume + change)*100))/5)) # arrondi au 0.05 près
            new_volume = round(new_volume / 100, 2)
        self.volume_label.text = str(int(new_volume*100))
        py.mixer.music.set_volume(new_volume)
        self.save_manager.data["music_volume"] = new_volume
        self.save_manager.save_data()        
    
    def enter(self, **kwargs):
        py.mixer.music.set_volume(self.saved_volume)
        py.mixer.music.play(-1, 0, 1000)
    
    def exit(self):
        print("leaving main menu")
        py.mixer.music.fadeout(2000)
 
    def draw(self, screen):
        self.draw_background(screen)
        title_surface = self.title_font.render("Mini Golf 2D", True, (255, 255, 255))
        title_surface_pos_x = self.WIDTH//2 - title_surface.get_width()//2
        title_surface_pos_y = self.HEIGHT//2- 175
        screen.blit(title_surface, (title_surface_pos_x, title_surface_pos_y))

        self.volume_label.draw(screen)

        for button in self.buttons:
            button.draw(screen)
    
    def draw_background(self, screen):
        CELL_SIZE = 50
        screen.fill((131, 177, 73))
        for i in range(self.WIDTH // CELL_SIZE):
            for j in range (self.HEIGHT // CELL_SIZE):
                if (i + j) %2 == 0:
                    py.draw.rect(screen, (161, 197, 75), (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 0 )
    
    def handle_events(self, events):
        for button in self.buttons:
            button.handle_events(events)
            
    def play(self, *args):
        self.state_manager.set_state(name="level_selection_menu")#, level="level_1"
    
    def exit_game(self, *args):
        py.event.post(py.event.Event(py.QUIT))
        