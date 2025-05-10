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
        if name in self.levels:
            return self.levels[name]
        return None