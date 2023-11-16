import random
import time
from .ant import Larva, Ant , ForagerAnt, NurseAnt, WorkerAnt, SlaveAnt, MaleAnt

class Queen:
    def __init__(self):
        self.laying_rate = 0.1

    def lay_eggs(self): 
        if random.random() < self.laying_rate:
            return Larva()

    def accept_new_ant(self, ant):
        print(f"La reine à accepté une nouvellle fourmi ({ant.ant_type}).")

class AntColony:
    def __init__(self):
        self.queen = Queen()
        self.larvae = []
        self.time = 0

    def simulate_time_passing(self, time_units):
        for _ in range(time_units):
            self.time += 1
            print(f"Temps passé: {self.time} unité(s)")

            new_larva = self.queen.lay_eggs()
            if new_larva:
                print("La reine a pondu un œuf.")
                self.larvae.append(new_larva)

            self.queen.lay_eggs()
            for larva in self.larvae:
                larva.age += 1
                if larva.age >= larva.time_to_hatch:
                    new_ant = larva.hatch()
                    print(f"Une nouvelle fourmi ({new_ant.ant_type}) est née!")
                    self.queen.accept_new_ant(new_ant)
                    self.larvae.remove(larva)
    def get_larva_count(self):
        return len(self.larvae)

    def get_ant_count(self):
        return sum(1 for larva in self.larvae if larva.age >= larva.time_to_hatch)

