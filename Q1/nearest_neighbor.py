#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 13:48:00 2024

@author: pierreadrienlefevre
"""



import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import seaborn as sns
from verypy.cvrp_io import read_TSPLIB_CVRP


def calculate_tour_cost(matrix, tour):
    total_cost = 0
    for i in range(len(tour) - 1):
        total_cost += matrix[tour[i]][tour[i + 1]]
    return total_cost



Test = read_TSPLIB_CVRP('Q1.tsp')
distance_matrix = Test.distance_matrix
print(distance_matrix)
# Coordonnées des villes
villes_coords = np.array([
    (21, 30),  # Ville 1
    (39, 15),  # Ville 2
    (31, 45),  # Ville 3
    (35, 41),  # Ville 4
    (35, 20),  # Ville 5
    (6, 46),   # Ville 6
    (28, 33),  # Ville 7
    (13, 16),  # Ville 8
    (1, 31),   # Ville 9
    (21, 34)   # Ville 10
])

# Calcul de la matrice des distances euclidiennes
matrice_distances = cdist(villes_coords, villes_coords, metric='euclidean')

def nearest_neighbor(matrix, start=0):
    n = len(matrix)
    visités = [False] * n
    tour = [start]
    visités[start] = True
    Iteration = 1
    
    for _ in range(1, n):
        last = tour[-1]
        
        next_city = np.argmin([matrix[last][j] if not visités[j] else np.inf for j in range(n)])
        tour.append(next_city)
        visités[next_city] = True
        
        # Visualisation à chaque itération avec le dernier point relié au premier
        plt.figure(figsize=(10, 10))
        sns.scatterplot(x=villes_coords[:, 0], y=villes_coords[:, 1], marker='o', color='blue', s=100)
        for i, coord in enumerate(villes_coords):
            plt.text(coord[0] + 0.5, coord[1], f'Ville {i+1}', fontsize=9)
        
        # Dessiner le tour partiel avec la dernière connexion
        for i in range(1, len(tour)):
            start_pos = villes_coords[tour[i-1]]
            end_pos = villes_coords[tour[i]]
            plt.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], 'r-')
        # Relier le dernier point au premier pour fermer le tour
        if len(tour) > 1:
            plt.plot([villes_coords[tour[-1]][0], villes_coords[tour[0]][0]], 
                     [villes_coords[tour[-1]][1], villes_coords[tour[0]][1]], 'r--')
        
        plt.title(f"Construction du tour des villes à l'itération {Iteration}")
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()
        
        Iteration += 1
        
    tour.append(start)  # Revenir au point de départ pour fermer le tour
    return tour

# Application de l'heuristique du plus proche voisin avec la matrice des distances
route = nearest_neighbor(matrice_distances, start=0)

distance = calculate_tour_cost(distance_matrix, route )




# =============================================================================
# Affichage
# =============================================================================
print(route)
print(distance)




