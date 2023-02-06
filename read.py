import json

class readfile():
    def __init__(self):
        self.measurements = {}
        file = "result.json"

        # Opening JSON file
        f = open(file, "r", encoding="UTF-8")

        content = f.read()
        
        # returns JSON object as 
        # a dictionary
        data = json.loads(content)

        self.measurements = data
        
        # Closing file
        f.close()