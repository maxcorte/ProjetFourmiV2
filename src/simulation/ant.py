import random

class Larva:
    def __init__(self,x,y):
        self.__time_to_hatch = random.randint(5, 10)  # Random time for larva to hatch
        self.__age = 0
        self.__position = x,y
        self.__id = 0

    @property
    def time_to_hatch(self):
        return self.__time_to_hatch
    @property
    def age(self):
        return self.__age
    @property
    def position(self):
        return self.__position
    @property
    def id(self):
        return self.__id
    def ajout_age(self):
        self.__age += 1
    @time_to_hatch.setter
    def time_to_hatch(self,a,b):
        self.__time_to_hatch = random.randint(a,b)
    @position.setter
    def position(self,new_x,new_y):
        self.__position = new_x,new_y
    def hatch(self):
        ant_type = random.choice(["Male", "Nurse", "Slaver", "Slave", "Soldier"])
        return Ant(ant_type,10,400,400)

class Ant:
    def __init__(self, ant_type,height,x,y):
        self.ant_type = ant_type
        self.__id = 0
        self.__height = height
        self.__food = 100
        self.__dead = False
        self.__position = x,y
        self.__age = 0
    @property
    def hungry(self):
        return self.__food
    @property
    def dead(self):
        return self.__dead
    @property
    def position(self):
        return self.__position
    @hungry.setter
    def hungry(self,value):
        self.__food -= value
    @dead.setter
    def dead(self):
        self.__dead = True
    @position.setter
    def get_position(self):
        pass
class Queen(Ant):
    def __init__(self):
        super().__init__("Queen",10,200,200)
        self.__laying_rate = 0.4
        self.accepted_ants = []
    @property
    def laying_rate(self):
        return self.__laying_rate
    @laying_rate.setter
    def laying_rate(self,value):
        self.__laying_rate = value


    def lay_eggs(self):
        """
        .....

        PRE: ?
        POST: ?
        """
        if random.random() < self.laying_rate:
            return Larva(300,300)

    def accept_new_ant(self, ant):
        print(f"La reine a accepté une nouvelle fourmi ({ant.ant_type}).")
        self.accepted_ants.append(ant)


class MaleAnt(Ant):
    def __init__(self):
        super().__init__("Male")
        # Add any specific attributes or methods for MaleAnt

class NurseAnt(Ant):
    def __init__(self):
        super().__init__("Nurse")
        self.__nurse_augment = 0.1
        # Add any specific attributes or methods for NurseAnt
    @property
    def nurse_augment(self):
        return self.__nurse_augment
    @nurse_augment.setter
    def nurse_augment(self, value):
        self.__nurse_augment = value

class SlaverAnt(Ant):
    def __init__(self):
        super().__init__("Slaver")
        # Add any specific attributes or methods for ForagerAnt
        self.__add_slave = random.randint(1,5)
        self.__survive_rate = 0.2
    @property
    def survive_rate(self):
        return self.__survive_rate
    @survive_rate.setter
    def survive_rate(self,value):
        self.__survive_rate = value
    def go_outside_slaver(self):
        pass
    def come_back_slaver(self):
        pass


class SlaveAnt(Ant):
    def __init__(self):
        super().__init__("Slave")
        # Add any specific attributes or methods for SlaveAnt
        self.__revolt_rate = 0.05
    @property
    def revolt_rate(self):
        return self.__revolt_rate
    @revolt_rate.setter
    def revolt_rate(self,value):
        self.__revolt_rate = value
    def revolt(self):
        if random.random() < self.__revolt_rate:
                pass


class SoldierAnt(Ant):
    def __init__(self):
        super().__init__("Soldier")
        # Add any specific attributes or methods for SlaveAnt
        self.__defense = 0.1
        self.__exit = False
        self.__survive_rate= 0.4
        self.__dig_speed = dig_speed

    @property
    def defense(self):
        return self.__defense
    @property
    def exit(self):
        return self.__exit
    @property
    def survive_rate(self):
        return self.__survive_rate
    @property
    def dig_speed(self):
        return self.__dig_speed

    @defense.setter
    def defense_modify(self, value):
        self.__defense = value
    @survive_rate.setter
    def survive_rate_modify(self,value):
        self.__survive_rate = value
    @dig_speed.setter
    def dig_speed_modify(self,value):
        self.__dig_speed = value
