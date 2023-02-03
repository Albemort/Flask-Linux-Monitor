import json

class readfile():
    def __init__(self):
        self.measurements = []
        file = "result.json"

        # Opening JSON file
        f = open(file, "r", encoding="UTF-8")

        content = f.read()

        x = content.replace("'", '"')
        
        # returns JSON object as 
        # a dictionary
        data = json.loads(x)

        self.measurements.append(data["physical_and_logical_cpu_count"])
        self.measurements.append(data["cpu_load (%)"])
        self.measurements.append(data["ram (Gb)"]["total_ram"])
        self.measurements.append(data["ram (Gb)"]["used_ram"])
        self.measurements.append(data["ram (Gb)"]["free_ram"])
        self.measurements.append(data["disk (Gb)"]["total_disk_space"])
        self.measurements.append(data["disk (Gb)"]["used_disk_space"])
        self.measurements.append(data["disk (Gb)"]["free_disk_space"])
        self.measurements.append(data["network_latency (ms)"]["min"])
        self.measurements.append(data["network_latency (ms)"]["avg"])
        self.measurements.append(data["network_latency (ms)"]["max"])
        
        # Closing file
        f.close()