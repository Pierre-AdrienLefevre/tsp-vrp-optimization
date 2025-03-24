#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 13:48:00 2024

@author: pierreadrienlefevre

Description: Ce script implémente l'heuristique du plus proche voisin pour résoudre le problème du voyageur de commerce (TSP) 
à partir d'une matrice de distances entre les villes. Le script calcule également le coût total du tour trouvé et visualise 
le parcours à l'aide de Matplotlib et Seaborn. Le temps d'exécution du script est mesuré et rapporté en fonction du nombre de villes.
"""


import numpy as np
from LireFichierTSP import read_TSPLIB_CVRP
import time
from creation_graph import graph


# Enregistrer le temps de début
start_time = time.time()


def nearest_neighbor(matrix, start=0, trace_graph = True):
    n = len(matrix)
    visités = [False] * n
    tour = [start]
    visités[start] = True
    if trace_graph == True :
        graph(np.array(problem.coordinate_points),tour )
    for _ in range(1, n):
        last = tour[-1]
        next_city = np.argmin([matrix[last][j] if not visités[j] else np.inf for j in range(n)])
        tour.append(next_city)
        visités[next_city] = True
        if trace_graph == True :
            graph(np.array(problem.coordinate_points),tour)

    tour.append(start)  # Revenir au point de départ pour fermer le tour
    return tour

def calculate_tour_cost(matrix, tour):
    total_cost = 0
    for i in range(len(tour) - 1):
        total_cost += matrix[tour[i]][tour[i + 1]]
    return total_cost


# =============================================================================
# Data
# ============================================================================

problem = read_TSPLIB_CVRP('Q2_1.tsp')
distance_matrix = problem.distance_matrix

# =============================================================================
# Main
# =============================================================================

# Application de l'heuristique du plus proche voisin avec la matrice des distances
route = nearest_neighbor(distance_matrix, start=0, trace_graph= True)
distance = calculate_tour_cost(distance_matrix, route )

# =============================================================================
# Modification pour affichage
# =============================================================================
# Vérifier si le premier élément de la liste est 0
if route[0] == 0:
    # Si oui, incrémenter chaque élément de la liste de 1
    route = [x + 1 for x in route]
# Sinon, ne rien faire (la liste reste inchangée)

# Vérifier si le premier élément de la liste est déjà 1
if route[0] != 1:
    # Trouver l'index de 1 dans la route
    index_of_one = route.index(1)

    # Réarranger la route pour commencer par 1, en supprimant le 1 final si nécessaire
    route = route[index_of_one:] + route[:index_of_one]
    if route[-1] == 1:
        route.pop()  # Supprime le dernier élément si c'est 1 pour éviter la répétition

    # Ajouter 1 à la fin si nécessaire pour boucler le retour au point de départ
    if route[-1] != 1:
        route.append(1)
    

# =============================================================================
# Temps d'execution
# =============================================================================
# Enregistrer le temps de fin
end_time = time.time()

# Calculer le temps d'exécution
execution_time = end_time - start_time
num_points = distance_matrix.shape[0]

# Calculer le temps d'exécution par point
time_per_point = execution_time / num_points


# =============================================================================
# Affichage
# =============================================================================
print(f"La route est : {route}")
print(f"La distance totale est : {distance}")
graph(np.array(problem.coordinate_points),route, distance)

print(f"Le temps d'exécution total est de {execution_time} secondes.")
print(f"Le temps d'exécution par point est de {time_per_point} secondes par point.")




#%%
