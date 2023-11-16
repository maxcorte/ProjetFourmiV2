import random

class Larva:
    def __init__(self):
        self.time_to_hatch = random.randint(5, 10)  # Random time for larva to hatch
        self.age = 0

    def hatch(self):
        ant_type = random.choice(["Male", "Worker", "Nurse", "Forager", "Slave"])
        return Ant(ant_type)

class Ant:
    def __init__(self, ant_type):
        self.ant_type = ant_type