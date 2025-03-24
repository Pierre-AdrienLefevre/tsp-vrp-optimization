#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:08:13 2024

@author: pierreadrienlefevre
"""


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def graph(coords, tour, distance=None, iteration=None, nom_algo = None):
    
    coordinates_df = pd.DataFrame(coords, columns=["x", "y"])
    coords = coordinates_df.values
    
    # Vérifier si le premier élément de la liste est 0
    if tour[0] == 0:
        # Si oui, incrémenter chaque élément de la liste de 1
        tour = [x + 1 for x in tour]
    # Sinon, ne rien faire (la liste reste inchangée)

    # Vérifier si le premier élément de la liste est déjà 1
    if tour[0] != 1:
        # Trouver l'index de 1 dans la route
        index_of_one = tour.index(1)
    
        # Réarranger la route pour commencer par 1, en supprimant le 1 final si nécessaire
        tour = tour[index_of_one:] + tour[:index_of_one]
        if tour[-1] == 1:
            tour.pop()  # Supprime le dernier élément si c'est 1 pour éviter la répétition
    
        # Ajouter 1 à la fin si nécessaire pour boucler le retour au point de départ
        if tour[-1] != 1:
            tour.append(1)

    
    # Ajuster les indices de tour pour la base zéro
    adjusted_tour = [t-1 for t in tour]  # Soustraire 1 de chaque élément de tour
    adjusted_tour = np.array(adjusted_tour)  # Convertir en array numpy pour l'indexation

    # Configurer le style Seaborn pour le graphique
    sns.set(style="darkgrid")


    plt.figure(figsize=(10, 10))

    # Tracer les points avec Seaborn
    sns.scatterplot(x=coords[:, 0], y=coords[:, 1], color='blue', s=100)

    # Mettre en évidence le point de départ en rouge
    plt.scatter(coords[adjusted_tour[0], 0], coords[adjusted_tour[0], 1], color='red', s=100, zorder=5)

    # Tracer le parcours en utilisant Matplotlib pour connecter les points
    for i in range(len(adjusted_tour)-1):
        plt.plot(coords[adjusted_tour[i:i+2], 0], coords[adjusted_tour[i:i+2], 1], '-o', color='blue')

    # Ajout du numéro des points avec un décalage
    offset_x = max(coords[:, 0]) * 0.005  # Légère augmentation du décalage pour la visibilité
    offset_y = max(coords[:, 1]) * 0.005
    for i, (x, y) in enumerate(coords):
        plt.text(x + offset_x, y + offset_y, str(i + 1), color='black', fontsize=10)
    
    if iteration is not None : 
        plt.title(f'Tour à l\'itération {iteration} de l\'algorithme {nom_algo} avec distance = {distance}' if distance is not None else 'Tour final')
    else:
        plt.title(f'Tour final de l\'algorithme {nom_algo} avec distance = {distance}' if distance is not None else 'Tour final')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(['Parcours'], loc='best')

    # Afficher le graphique
    plt.show()
    
    
