import json
class LevelManager:
    def __init__(self, path):
        self.levels = {}
        self.load_all_level(path)

    def load_all_level(self, path):
        with open(path) as file:
            self.levels = json.load(file)
            file.close()
    
    def get_level(self, name:str):
        return self.levels[name]