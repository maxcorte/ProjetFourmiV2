import argparse
import time
from simulation.colony import AntColony
from gui import run_simulation_gui

def run_simulation_cli(ant_colony, simulation_time):
    #ant_colony = AntColony()

    for _ in range(int(simulation_time)):
        ant_colony.simulate_time_passing(1)
        time.sleep(1)

    larva_count = ant_colony.get_larva_count()
    ant_count = ant_colony.get_ant_count()
    print(f"Nombre de larves: {larva_count}")
    print(f"Nombre de fourmis: {ant_count}")

def main(ant_colony):
    parser = argparse.ArgumentParser(description='Simulation de gestion de colonie de fourmis')
    parser.add_argument('--temps_simulation', type=float, help='Temps de simulation')
    parser.add_argument('--gui', action='store_true', help='Lancer l\'interface graphique')

    args = parser.parse_args()

    #ant_colony = AntColony()

    if args.gui:
        run_simulation_gui()
    else:
        run_simulation_cli(ant_colony, args.temps_simulation)

    afficher_types_fourmis = input("Afficher les types de fourmis générés pendant la simulation ? (Oui/Non): ").lower()
    if afficher_types_fourmis == "oui":
        ant_colony.show_generated_ant_types()



if __name__ == "__main__":
    ant_colony = AntColony()
    main(ant_colony)





