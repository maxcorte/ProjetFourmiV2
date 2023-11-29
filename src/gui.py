# gui.py
import pygame
from pygame_widgets.textbox import TextBox
from pygame.locals import QUIT
from simulation.colony import AntColony
import random

def run_simulation_gui(ant_colony):
    pygame.init()
    screen_info = pygame.display.Info()
    WINDOW_WIDTH, WINDOW_HEIGHT = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simulation de Colonie de Fourmis")
    background_color = (34, 139, 34)  # Vert Forêt
    ant_colony.queen.position = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        screen.fill(background_color)
        pygame.draw.rect(screen, (255, 255, 255), (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100, 200, 200))
        pygame.draw.rect(screen, (255, 255, 255), (WINDOW_WIDTH // 2 -50, WINDOW_HEIGHT // 2 +100, 100, WINDOW_HEIGHT//2-100))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 6))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 6), 5)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 10)
        pygame.draw.circle(screen, (139, 0, 0), ant_colony.queen.position, 10)
# --------------------------------------------- Légende ------------------------------------------------------
        #reine
        pygame.draw.circle(screen, (139, 0, 0), [WINDOW_WIDTH-140,50], 10)
        text_surface = font.render("= Reine", True, (0, 0, 0))
        screen.blit(text_surface, (WINDOW_WIDTH - 120, 35))
        #adfafa
# ---------------------------------------------- Larves --------------------------------------------------------
        new_larva = ant_colony.queen.lay_eggs()

        if new_larva:
            collides = False
            new_larva_rect = pygame.Rect(new_larva.position[0], new_larva.position[1], 7, 7)
            for larva in ant_colony.larvae:
                existing_larva_rect = pygame.Rect(larva.position[0], larva.position[1], 7, 7)
                if existing_larva_rect.colliderect(new_larva_rect):
                    collides = True
                    break
            # Si aucune collision n'a été trouvée, ajouter la nouvelle larve à la colonie
            if not collides:
                new_larva.position = (
                    random.randint(WINDOW_WIDTH // 2 - 10, WINDOW_WIDTH // 2 + 10),
                    random.randint(WINDOW_HEIGHT // 2 + 30, WINDOW_HEIGHT // 2 + 60)
                )
                ant_colony.add_larva(new_larva)

        larvae_to_remove = []
            # Dessiner toutes les larves de la colonie sur l'écran
        for larva in ant_colony.larvae:
            pygame.draw.circle(screen, (0, 0, 0), larva.position, 3)
            larva.ajout_age()
            if larva.age >= larva.time_to_hatch:
                larvae_to_remove.append(larva)
                new_ant = larva.hatch()
                ant_key = new_ant.ant_type
                ant_colony.dicAnt[ant_key] = (new_ant, larva.position[0], larva.position[1])

# ---------------------------------------------- Fourmis --------------------------------------------------------
        for larva in larvae_to_remove:
            ant_colony.larvae.remove(larva)
        for ant_key, (ant, x, y) in ant_colony.dicAnt.items():
            pygame.draw.circle(screen, (0, 0, 255), (x, y), 3)





        larva_text= font.render(str(ant_colony.larvae), True, (0, 0, 0))
        screen.blit(larva_text, (50, 35))
        ant_text= font.render(str(ant_colony.dicAnt), True, (0, 0, 0))
        screen.blit(ant_text, (50, 135))

        pygame.display.flip()
        clock.tick(1)  # Limite le nombre d'images par seconde

    pygame.quit()

