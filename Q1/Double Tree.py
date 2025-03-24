#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:56:40 2024

@author: pierreadrienlefevre
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Coordonnées des villes
coords = np.array([
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

# Calcul de la matrice des distances
def calculate_distance_matrix(coords):
    n = len(coords)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))
    return distance_matrix

distance_matrix = calculate_distance_matrix(coords)

# Création du graphe à partir de la matrice des distances
G = nx.Graph()
for i in range(len(coords)):
    for j in range(i + 1, len(coords)):
        G.add_edge(i, j, weight=distance_matrix[i][j])

plt.figure(figsize=(10, 8))
# Définition des positions des noeuds basées sur coords
pos = {i: coords[i] for i in range(len(coords))}

# Dessiner le graphe
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15)

# Formater les poids des arêtes pour afficher uniquement deux décimales
edge_labels = {(i, j): f"{d['weight']:.2f}" for i, j, d in G.edges(data=True)}

# Dessiner les poids des arêtes avec deux décimales
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title('Arbre de départ')
plt.show()



# Calcul de l'arbre de recouvrement minimum (MST)
mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

# Affichage de l'arbre de recouvrement minimum
plt.figure(figsize=(10, 8))
pos = {i: coords[i] for i in range(len(coords))}
labels = nx.get_edge_attributes(mst, 'weight')
nx.draw(mst, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
nx.draw_networkx_edge_labels(mst, pos, edge_labels=labels)
plt.title('Arbre de recouvrement minimum (MST) avec Algorithme de Kruskal')
plt.show()


#----------------------------------------------------------

# Pour doubler chaque arête de l'MST, on crée un nouveau graphe
double_mst = nx.MultiGraph(mst)

# On ajoute les mêmes arêtes une fois de plus pour "doubler"
for u, v, data in mst.edges(data=True):
    double_mst.add_edge(u, v, weight=data['weight'])

# Vérifier si le graphe est eulerien (chaque sommet a un degré pair)
is_eulerian = nx.is_eulerian(double_mst)

# Ajustement des positions pour visualiser le dédoublement des arêtes
def adjust_positions(pos, offset=(0.6, 0.4)):
    pos_adjusted = {}
    for node, (x, y) in pos.items():
        pos_adjusted[node] = (x + offset[0], y + offset[1])
    return pos_adjusted

# Positions originales
pos = {i: coords[i] for i in range(len(coords))}

# Positions ajustées pour le dédoublement
pos_adjusted = adjust_positions(pos)

# Affichage de l'arbre de recouvrement minimum avec les positions ajustées
plt.figure(figsize=(10, 8))
nx.draw(mst, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', label='Original MST')
nx.draw(mst, pos_adjusted, with_labels=False, node_color='skyblue', node_size=0, edge_color='red', style='dashed', label='Adjusted MST')
plt.title('Arbre de recouvrement minimum (MST) avec arêtes dédoublées')
plt.show()

#-----------------------------------------


# Trouver un circuit eulerien dans le graphe eulerien
eulerian_circuit = list(nx.eulerian_circuit(double_mst, source=0))


# Afficher le circuit eulerien sous forme de séquence de villes visitées
eulerian_circuit_sequence = [u for u, v in eulerian_circuit]
eulerian_circuit_sequence.append(eulerian_circuit[-1][1])  # Ajouter la dernière ville pour boucler le circuit
print(eulerian_circuit_sequence)


def create_hamiltonian_tour(eulerian_circuit):
    visited = set()  # Pour garder une trace des villes déjà visitées
    hamiltonian_tour = []  # Le tour hamiltonien à construire

    for city in eulerian_circuit:
        if city not in visited:
            hamiltonian_tour.append(city)
            visited.add(city)
    
    hamiltonian_tour.append(eulerian_circuit[0])  # Ajouter le point de départ à la fin pour compléter le tour
    return hamiltonian_tour

# Créer le tour hamiltonien à partir du circuit eulerien
hamiltonian_tour = create_hamiltonian_tour(eulerian_circuit_sequence)




# Calculer le coût total du tour hamiltonien
def calculate_hamiltonian_tour_cost(matrix, tour):
    total_cost = 0
    for i in range(len(tour) - 1):
        total_cost += matrix[tour[i]][tour[i + 1]]
    return total_cost

# Calcul du coût total du tour hamiltonien
hamiltonian_tour_cost = calculate_hamiltonian_tour_cost(distance_matrix, hamiltonian_tour)

# Affichage du coût total du tour hamiltonien
print(hamiltonian_tour_cost)

# Afficher la séquence du tour hamiltonien
print(hamiltonian_tour)

# Création d'un sous-graphe pour le chemin
path_graph = nx.Graph()
for i in range(len(hamiltonian_tour) - 1):
    node_start = hamiltonian_tour[i]
    node_end = hamiltonian_tour[i + 1]
    # Ajout de l'arête avec le poids correspondant du graphe original
    weight = G[node_start][node_end]['weight']
    path_graph.add_edge(node_start, node_end, weight=weight)

# Affichage du graphe avec le chemin spécifié
plt.figure(figsize=(10, 8))

# Dessiner le graphe original
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', width=1, font_size=15)

# Dessiner le sous-graphe du chemin pour le mettre en évidence
edge_colors = ['red' if (u, v) in path_graph.edges or (v, u) in path_graph.edges else 'gray' for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, edgelist=path_graph.edges, edge_color='red', width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in path_graph.edges(data=True)})

plt.title(f"Chemin final de l'algortime Double Tree avec distance = {hamiltonian_tour_cost}")
plt.show()



