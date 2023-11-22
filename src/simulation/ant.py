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


class MaleAnt(Ant):
    def __init__(self):
        super().__init__("Male")
        # Add any specific attributes or methods for MaleAnt

class WorkerAnt(Ant):
    def __init__(self):
        super().__init__("Worker")
        # Add any specific attributes or methods for WorkerAnt

class NurseAnt(Ant):
    def __init__(self):
        super().__init__("Nurse")
        # Add any specific attributes or methods for NurseAnt

class ForagerAnt(Ant):
    def __init__(self):
        super().__init__("Forager")
        # Add any specific attributes or methods for ForagerAnt

class SlaveAnt(Ant):
    def __init__(self):
        super().__init__("Slave")
        # Add any specific attributes or methods for SlaveAnt
class Queen(ant):
    def __init__(self):
        super().__init__("Queen")
        self.__laying_rate = 0.4

    def laying_rate(self):
        return self.__laying_rate
    def lay_eggs(self):
        if random.random() < self.laying_rate:
            return Larva()

    def accept_new_ant(self, ant):
        print(f"La reine à accepté une nouvellle fourmi ({ant.ant_type}).")