import pygame as py

class AssetsManager:
    def __init__(self):
        self.assets = {}
    def load(self, name, path):
        if name not in self.assets:
            self.assets[name] = py.image.load(path)
    def get(self, name):
        if name in self.assets:
            return self.assets[name]
