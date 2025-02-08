import pygame as py

class AssetsManager:
    def __init__(self):
        self.assets = {}
    def load(self, name, path):
        if name not in self.assets:
            self.assets[name] = py.image.load(path).convert_alpha()
    def get(self, name):
        if name in self.assets:
            return self.assets[name]
        
class SoundsManager:
    def __init__(self):
        self.sounds = {}
    def load(self, name, path):
        if name not in self.sounds:
            self.sounds[name] = py.mixer.Sound(path)
    def get(self, name):
        if name in self.sounds:
            return self.sounds[name]
