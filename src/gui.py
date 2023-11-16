# gui.py
import pygame
from pygame.locals import QUIT
from simulation.colony import AntColony

def run_simulation_gui():
    ant_colony = AntColony()

    pygame.init()
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Simulation de Colonie de Fourmis")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        ant_colony.simulate_time_passing(1)

        # Ajoutez ici le code pour mettre à jour l'interface graphique
        # en fonction de l'état actuel de la simulation
        # Par exemple, dessinez les fourmis, la reine, etc.

        pygame.display.flip()
        clock.tick(60)  # Limite le nombre d'images par seconde

    pygame.quit()

