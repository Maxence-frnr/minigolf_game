import json
class SaveManager:
    def __init__(self, path):
        self.data = {}
        self.load_all_data(path)

    def load_all_data(self, path):
        with open(path) as file:
            self.data = json.load(file)
            file.close()
    
    def get_data(self, name:str):
        return self.data[name]