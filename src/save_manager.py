import json
class SaveManager:
    def __init__(self, path):
        self.data = {}
        self.path = path
        self.load_all_data()

    def load_all_data(self):
        with open(self.path) as file:
            self.data = json.load(file)
            file.close()
    
    def get_data(self, name:str):
        return self.data[name]
    
    def save_data(self):
        #Serializing
        json_dict = json.dumps(self.data, indent=4)
        #Saving
        with open(self.path, "w") as file:
            file.write(json_dict)
            file.close()