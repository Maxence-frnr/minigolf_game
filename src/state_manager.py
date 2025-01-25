import pygame as py

class StateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
    
    def add_state(self, name, state):
        if name not in self.states:
            self.states[name] = state
    
    def set_state(self, name):
        if self.current_state:
            self.current_state.exit()
        if name in self.states:
            self.current_state = self.states[name]
            self.current_state.enter() # A ajouter a chaque etat

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)
    
    def update(self, dt): #dt = deltaTime
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

class BaseState:
    def __init__(self):
        pass
    def enter(self):
        #called when we enter this state
        pass

    def exit(self):
        #called when we exit this state
        pass

    def handle_events(self, events):
        pass 

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def update_window_size(self, screen):
        pass
    
    def on_mouse_motion(self, pos):
        pass
