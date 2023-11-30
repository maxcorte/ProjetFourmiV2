import random
import pygame
from pygame.locals import QUIT
from simulation.noise_map import generate_noise_map
from simulation.intelligence.male_ai import (
    move as male_move, action as male_action, check_color_and_adjust as male_check_color_and_adjust)
from simulation.intelligence.soldier_ai import (
    move as soldier_move, action as soldier_action, check_color_and_adjust as soldier_check_color_and_adjust)

noise_map = generate_noise_map(3440, 1440, scale=135, octaves=1, persistence=2, lacunarity=0.6, seed=2)


def run_simulation_gui(ant_colony):
    """
    Exécute une simulation graphique d'une colonie de fourmis.

    PRE:
    - ant_colony est une instance valide de la classe AntColony.

    POST:
    - Lance une simulation graphique de la colonie de fourmis avec une interface utilisateur.
    - Aucune modification permanente de l'état de la colonie n'est effectuée par cette fonction.
    """
    pygame.init()
    # --------------------------------------------- Infos screen ------------------------------------------------------
    screen_info = pygame.display.Info()
    window_width, window_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((window_width, window_height))
    # --------------------------------------------- Variables globales -----------------------------------------------
    pygame.display.set_caption("Simulation de Colonie de Fourmis")
    background_color = (34, 139, 34)  # Vert Forêt
    ant_colony.queen.position = (window_width // 2, window_height // 2)
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    digging_list = []
    running = True
    # --------------------------------------------- Début simulation ----------------------------------------------
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        screen.fill(background_color)
        # Dessiner la noise map

        for i in range(window_width):
            for j in range(window_height):
                value = int(noise_map[i][j] * 255)  # Convertir la valeur de bruit en une valeur de couleur
                color = (value, value, value)
                pygame.draw.rect(screen, color, (i, j, 1, 1))

        pygame.draw.rect(screen, (255, 255, 255), (window_width // 2 - 100, window_height // 2 - 100, 200, 200))
        pygame.draw.rect(screen, (255, 255, 255), (window_width // 2 - 50, window_height // 2 + 100, 100,
                                                   window_height // 2 - 100))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, window_width, window_height // 6))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, window_width, window_height // 6), 5)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, window_width, window_height), 10)
        pygame.draw.circle(screen, (139, 0, 0), ant_colony.queen.position, 10)
        for x, y in digging_list:
            pygame.draw.rect(screen, (255, 255, 255),
                             (x - 10, y - 10, 20, 20))
        # --------------------------------------------- Légende ------------------------------------------------------
        pygame.draw.circle(screen, (139, 0, 0), [window_width - 140, 50], 10)
        text_surface = font.render("= Reine", True, (0, 0, 0))
        screen.blit(text_surface, (window_width - 120, 35))
        # ---------------------------------------------- Larves --------------------------------------------------------
        new_larva = ant_colony.queen.lay_eggs()

        if new_larva:
            collides = False
            new_larva_rect = pygame.Rect(new_larva.position[0], new_larva.position[1], 20, 20)
            for larva in ant_colony.larvae:
                existing_larva_rect = pygame.Rect(larva.position[0], larva.position[1], 20, 20)
                if existing_larva_rect.colliderect(new_larva_rect):
                    collides = True
                    break
            # Si aucune collision n'a été trouvée, ajouter la nouvelle larve à la colonie
            if not collides:
                new_larva.position = (
                    random.randint(window_width // 2 - 50, window_width // 2 + 50),
                    random.randint(window_height // 2 + 10, window_height // 2 + 80)
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
                new_ant.id = larva.id
                ant_key = new_ant.id
                ant_colony.dicAnt[ant_key] = (new_ant, larva.position[0], larva.position[1], 0, 0)
        for larva in larvae_to_remove:
            ant_colony.larvae.remove(larva)
        # ---------------------------------------------- Fourmis ------------------------------------------------

        ants_to_remove = []
        for ant_key, (ant, x, y, count, move) in ant_colony.dicAnt.items():
            ant.age += 1
            if ant.age >= 1000:
                ant.dead = True
            if not ant.dead:
                if ant.ant_type == "Male":
                    new_x, new_y, count, move = male_move(x, y, count, move, window_width, window_height)
                    male_action()
                    move, count = male_check_color_and_adjust(new_x, new_y, move, count, window_width, window_height,
                                                              screen)
                    ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
                    pygame.draw.circle(screen, (165, 42, 42), (int(new_x), int(new_y)), 6)
                elif ant.ant_type == "Nurse":
                    pygame.draw.circle(screen, (255, 105, 180), (x, y), 6)
                elif ant.ant_type == "Slaver":
                    pygame.draw.circle(screen, (0, 0, 0), (x, y), 6)
                elif ant.ant_type == "Slave":
                    pygame.draw.circle(screen, (255, 255, 0), (x, y), 6)
                if ant.ant_type == "Soldier":
                    new_x, new_y, count, move = soldier_move(x, y, count, move, window_width, window_height)
                    soldier_action()

                    move, count = soldier_check_color_and_adjust(new_x, new_y, move, count, window_width,
                                                                 window_height, screen, noise_map, digging_list)

                    ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
                    pygame.draw.circle(screen, (0, 0, 255), (int(new_x), int(new_y)), 8)
            else:
                # Supprimer la fourmi de la colonie si elle est morte
                ants_to_remove.append(ant_key)
        for ant_key in ants_to_remove:
            del ant_colony.dicAnt[ant_key]
        # ---------------------------------------------- Texte --------------------------------------------------------
        larva_text = font.render(str(ant_colony.larvae), True, (0, 0, 0))
        screen.blit(larva_text, (50, 35))
        ant_text = font.render(str(ant_colony.dicAnt), True, (0, 0, 0))
        screen.blit(ant_text, (50, 135))

        pygame.display.flip()
        clock.tick(20)  # Limite le nombre d'images par seconde

    pygame.quit()
