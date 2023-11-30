import random
larva_id_count = 0
class Larva:
    def __init__(self,x,y,id_larva):
        self.time_to_hatch = random.randint(5, 10)  # Random time for larva to hatch
        self.age = 0
        self.position = x,y
        self.id = id_larva
    def ajout_age(self):
        self.age += 1
    def time_to_hatch(self,a,b):
        self.time_to_hatch = random.randint(a,b)
    def hatch(self):
        ant_type = random.choice(["Male", "Nurse", "Slaver", "Slave", "Soldier"])
        return Ant(ant_type,10,400,400,0)
class Ant:
    def __init__(self, ant_type, height, x, y, id_ant):
        self.ant_type = ant_type
        self.id = id_ant
        self.__height = height
        self.food = 100
        self.dead = False
        self.position = x, y
        self.age = 0
    def hungry(self,value):
        self.food -= value
    def eat(self,value):
        self.food += value
    def dead(self):
        self.dead = True
class Queen(Ant):
    def __init__(self):
        super().__init__("Queen",10,0, 0,0)
        self.laying_rate = 0.05
        self.accepted_ants = []
        self.generated_ant_types = []
    def set_laying_rate(self,value):
        self.laying_rate = value
    def lay_eggs(self):
        global larva_id_count
        """
        Simule la ponte d'œufs par la reine.

        PRE:
        - La reine existe.

        POST:
        - Si le nombre aléatoire généré est inférieur au taux de ponte (laying_rate),
          une nouvelle larve est créée avec un identifiant unique et renvoyée.
        - Si aucune nouvelle larve n'est créée, la méthode renvoie None.
        """
        if random.random() < self.laying_rate:
            larva_id_count += 1
            return Larva(0,0,larva_id_count)
    def accept_new_ant(self, ant):
        self.accepted_ants.append(ant)
class MaleAnt(Ant):
    def __init__(self):
        super().__init__("Male")
        # Add any specific attributes or methods for MaleAnt
class NurseAnt(Ant):
    def __init__(self):
        super().__init__("Nurse")
        self.nurse_augment = 0.1
        # Add any specific attributes or methods for NurseAnt
    def nurse_augment(self, value):
        self.nurse_augment = value
class SlaverAnt(Ant):
    def __init__(self):
        super().__init__("Slaver")
        # Add any specific attributes or methods for ForagerAnt
        self.add_slave = random.randint(1,5)
        self.survive_rate = 0.2
    def survive_rate(self,value):
        self.survive_rate = value
    def go_outside_slaver(self):
        pass
    def come_back_slaver(self):
        pass
class SlaveAnt(Ant):
    def __init__(self):
        super().__init__("Slave")
        # Add any specific attributes or methods for SlaveAnt
        self.revolt_rate = 0.05
    def revolt_rate(self,value):
        self.revolt_rate = value
    def revolt(self):
        if random.random() < self.revolt_rate:
                pass
class SoldierAnt(Ant):
    def __init__(self):
        super().__init__("Soldier")
        # Add any specific attributes or methods for SlaveAnt
        self.defense = 0.1
        self.exit = False
        self.survive_rate = 0.4
        self.dig_speed = 0.5
    def defense_modify(self, value):
        self.defense = value
    def survive_rate_modify(self, value):
        self.survive_rate = value
    def dig_speed_modify(self, value):
        self.dig_speed = value