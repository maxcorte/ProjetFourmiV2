import random
import time
from .ant import Queen, Larva, Ant, SlaverAnt, NurseAnt, SlaveAnt, MaleAnt,SoldierAnt


class AntColony:
    def __init__(self):
        self.__queen = Queen()
        self.__larvae = []
        self.__time = 0

    @property
    def queen(self):
        return self.__queen

    @property
    def larvae(self):
        return self.__larvae

    @property
    def time(self):
        return self.__time

    def simulate_time_passing(self, time_units):
        for _ in range(time_units):
            self.__time += 1
            print(f"Temps passé: {self.__time} unité(s)")

            new_larva = self.__queen.lay_eggs()
            if new_larva:
                print("La reine a pondu un œuf.")
                self.add_larva(new_larva)

            for larva in self.__larvae:
                larva.ajout_age()
                if larva.age >= larva.time_to_hatch:
                    new_ant = larva.hatch()
                    print(f"Une nouvelle fourmi ({new_ant.ant_type}) est née!")
                    self.__queen.accept_new_ant(new_ant)
                    self.remove_larva(larva)

    def get_larva_count(self):
        return len(self.__larvae)

    def get_ant_count(self):
        return sum(1 for larva in self.__larvae if larva.age >= larva.time_to_hatch) + len(self.__queen.accepted_ants)

    def add_larva(self, larva):
        self.__larvae.append(larva)

    def remove_larva(self, larva):
        self.__larvae.remove(larva)


