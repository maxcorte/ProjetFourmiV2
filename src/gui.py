# gui.py
import pygame
import math
from pygame_widgets.textbox import TextBox
from pygame.locals import QUIT
from simulation.colony import AntColony
import random
import noise


def run_simulation_gui(ant_colony):
    pygame.init()
# --------------------------------------------- Infos screen ------------------------------------------------------
    screen_info = pygame.display.Info()
    WINDOW_WIDTH, WINDOW_HEIGHT = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# --------------------------------------------- Variables globales ------------------------------------------------------
    pygame.display.set_caption("Simulation de Colonie de Fourmis")
    background_color = (34, 139, 34)  # Vert Forêt
    ant_colony.queen.position = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    digging_list = []
    running = True
    noise_map = generate_noise_map(WINDOW_WIDTH, WINDOW_HEIGHT, scale=20, octaves=6, persistence=0.5, lacunarity=2.0,
                                   seed=1)
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
        for x, y in digging_list:
            pygame.draw.rect(screen, (255, 255, 255),
                             (x - 15, y - 15, 30, 30))
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
            new_larva_rect = pygame.Rect(new_larva.position[0], new_larva.position[1], 20, 20)
            for larva in ant_colony.larvae:
                existing_larva_rect = pygame.Rect(larva.position[0], larva.position[1], 20, 20)
                if existing_larva_rect.colliderect(new_larva_rect):
                    collides = True
                    break
            # Si aucune collision n'a été trouvée, ajouter la nouvelle larve à la colonie
            if not collides:
                new_larva.position = (
                    random.randint(WINDOW_WIDTH // 2 - 50, WINDOW_WIDTH // 2 + 50),
                    random.randint(WINDOW_HEIGHT // 2 + 10, WINDOW_HEIGHT // 2 + 80)
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

# ---------------------------------------------- Fourmis --------------------------------------------------------
        for larva in larvae_to_remove:
            ant_colony.larvae.remove(larva)
        for ant_key, (ant, x, y, count, move) in ant_colony.dicAnt.items():
            if ant.ant_type == "Male":
                if not ant.dead:
                    # Choisir un mouvement aléatoire
                    if count == 0:
                        random_move = random.randint(0, 3)
                        if random_move == 0:
                            angle = 0  # vers la droite
                        elif random_move == 1:
                            angle = math.pi / 2  # vers le haut
                        elif random_move == 2:
                            angle = math.pi  # vers la gauche
                        elif random_move == 3:
                            angle = 3 * math.pi / 2  # vers le bas
                        distance = 10
                        move = angle
                        count = random.randint(7, 12)

                    if count != 0:
                        angle = move
                        distance = 10
                        count -= 1

                    # Calculer les nouvelles coordonnées en fonction de la direction
                    new_x = x + distance * math.cos(angle)
                    new_y = y + distance * math.sin(angle)

                    if not (30 <= new_x <= WINDOW_WIDTH-30 and WINDOW_HEIGHT/6+30 <= new_y <= WINDOW_HEIGHT-30):
                        # Inverser la direction en ajoutant ou soustrayant π (pi)
                        angle += math.pi
                        # Recalculer les nouvelles coordonnées avec la direction inversée
                        new_x = x + distance * math.cos(angle)
                        new_y = y + distance * math.sin(angle)

                    color_under_ant = screen.get_at((int(new_x), int(new_y)))
                    if color_under_ant == (34, 139, 34):
                        move = angle - math.pi  # Inverser la direction si la couleur sous la fourmi est verte
                        count = random.randint(7, 12)

                    # Mettre à jour la position de la fourmi
                    ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
                    pygame.draw.circle(screen, (165, 42, 42), (int(new_x), int(new_y)), 6)
                else:
                    pygame.draw.circle(screen, (0, 0, 0), (x, y), 0)
            elif ant.ant_type == "Nurse":

                pygame.draw.circle(screen, (255,105,180), (x, y), 6)
            elif ant.ant_type == "Slaver":
                pygame.draw.circle(screen, (0,0,0), (x, y), 6)
            elif ant.ant_type == "Slave":
                pygame.draw.circle(screen, (255,255,0), (x, y), 6)
            elif ant.ant_type == "Soldier":
                if not ant.dead:
                    # Choisir un mouvement aléatoire
                    if count == 0:
                        random_move = random.randint(0, 3)
                        if random_move == 0:
                            angle = 0  # vers la droite
                        elif random_move == 1:
                            angle = math.pi / 2  # vers le haut
                        elif random_move == 2:
                            angle = math.pi  # vers la gauche
                        elif random_move == 3:
                            angle = 3 * math.pi / 2  # vers le bas
                        distance = 10
                        move = angle
                        count = random.randint(7, 12)

                    if count != 0:
                        angle = move
                        distance = 10
                        count -= 1

                    # Calculer les nouvelles coordonnées en fonction de la direction
                    new_x = x + distance * math.cos(angle)
                    new_y = y + distance * math.sin(angle)

                    if not (30 <= new_x <= WINDOW_WIDTH-30 and WINDOW_HEIGHT/6+30 <= new_y <= WINDOW_HEIGHT-30):
                        # Inverser la direction en ajoutant ou soustrayant π (pi)
                        angle += math.pi
                        # Recalculer les nouvelles coordonnées avec la direction inversée
                        new_x = x + distance * math.cos(angle)
                        new_y = y + distance * math.sin(angle)

                    color_under_ant = screen.get_at((int(new_x), int(new_y)))

                    # Utiliser la carte de bruit pour déterminer si la fourmi doit creuser
                    noise_value = noise_map[int(new_x)][int(new_y)]
                    digging_threshold = 0.5  # Ajustez ce seuil selon vos besoins
                    if color_under_ant == (34, 139, 34) and noise_value > digging_threshold:
                        digging_list.append((int(new_x), int(new_y)))

                    # Mettre à jour la position de la fourmi
                    ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
                    pygame.draw.circle(screen, (0, 0, 255), (int(new_x), int(new_y)), 8)
                else:
                    pygame.draw.circle(screen, (0, 0, 0), (x, y), 0)

        # ---------------------------------------------- Texte --------------------------------------------------------




        larva_text= font.render(str(ant_colony.larvae), True, (0, 0, 0))
        screen.blit(larva_text, (50, 35))
        ant_text= font.render(str(ant_colony.dicAnt), True, (0, 0, 0))
        screen.blit(ant_text, (50, 135))

        pygame.display.flip()
        clock.tick(60)  # Limite le nombre d'images par seconde

    pygame.quit()

