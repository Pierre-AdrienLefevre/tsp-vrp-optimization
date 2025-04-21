#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 22:23:13 2024

@author: pierreadrienlefevre
"""
"Assurez vous d'avoir dans le meme dossier les fichiers LireFichierTSP"
"et creation_graph et le dossier verypy"
'Installer les packages suivants :'

'pip install numpy'
'pip install matplotlib'
'pip install seaborn'
'pip install scipy'
'pip install pandas'

from builtins import range
from itertools import groupby    
from logging import log, DEBUG
from verypy.util import routes2sol, objf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from TSPFile_reader import read_TSPLIB_CVRP
from verypy.config import CAPACITY_EPSILON as C_EPS
from verypy.config import COST_EPSILON as S_EPS
import time
from creation_graph import graph


# Enregistrer le temps de début
start_time = time.time()


def sol2routes(sol):
    """Convert  solution to a list of routes (each a list of customers leaving 
    and returning to a depot (node 0). Removes empty routes. WARNING: this also 
    removes other concecutive duplicate nodes, not just 0,0!"""
    if not sol or len(sol)<=2: return []
    return [[0]+list(r)+[0] for x, r in groupby(sol, lambda z: z == 0) if not x]

def clarke_wright_savings_function(D):
    N = len(D)
    n = N-1
    savings = [None]*int((n*n-n)/2)
    idx = 0
    for i in range(1,N):
        for j in range(i+1,N):
            s = D[i,0]+D[0,j]-D[i,j]
            savings[idx] = (s,-D[i,j],i,j)
            idx+=1
    savings.sort(reverse=True)
    #print(savings)
    return savings 

def update_plot(routes, coordinates):
    plt.clf()  # Efface la figure actuelle

    # Appliquer le thème de Seaborn pour le style
    sns.set_theme()
    
    plt.figure(figsize=(12, 8))
    
    # Tracé des villes avec Seaborn
    sns.scatterplot(x=coordinates[:, 0], y=coordinates[:, 1], color='blue', s=100, label='Villes', zorder=5)
    
    # Ajout du numéro des points avec un décalage
    offset_x = max(coordinates[:, 0]) * 0.001  # Décalage en X basé sur 1% de la gamme
    offset_y = max(coordinates[:, 1]) * 0.001  # Décalage en Y basé sur 1% de la gamme
    for i, (x, y) in enumerate(coordinates):
       plt.text(x + offset_x, y + offset_y, str(i), color='red', fontsize=9)
       

    for route in routes:
        if route:  # Vérifie si l'itinéraire n'est pas vide
            # Ajoute le point de départ au début et à la fin de l'itinéraire pour boucler
            route_with_depot = [0] + route + [0]
            route_coords = np.array([coordinates[i] for i in route_with_depot])
            
            # Tracé de l'itinéraire avec Matplotlib pour garder l'ordre des points
            plt.plot(route_coords[:, 0], route_coords[:, 1], marker='o', linestyle='-', linewidth=2, markersize=5)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Visualisation des itinéraires VRP ')
    plt.pause(0.01)  # Permet la mise à jour de l'affichage
    plt.show(block=False)  # Affiche sans bloquer le code suivant

def parallel_savings_init(D, d, C, L=None, minimize_K=False,
                          savings_callback=clarke_wright_savings_function, trace_graph = False):

    # Configuration initiale du graphique
    plt.ion()  # Active le mode interactif
    plt.figure(figsize=(10, 6))
    
    N = len(D)
    ignore_negative_savings = not minimize_K
    
    ## 1. make route for each customer
    routes = [[i] for i in range(1,N)]
    route_demands = d[1:] if C else [0]*N
    if L: route_costs = [D[0,i]+D[i,0] for i in range(1,N)]
    
    try:
        ## 2. compute initial savings 
        savings = savings_callback(D)
        
        # zero based node indexing!
        endnode_to_route = [0]+list(range(0,N-1))
        
        ## 3. merge
        # Get potential merges best savings first (second element is secondary
        #  sorting criterion, and it it ignored)
        for best_saving, _, i, j in savings:
            #if __debug__:
               # log(DEBUG-1, "Popped savings s_{%d,%d}=%.2f" % (i,j,best_saving))
                
            if ignore_negative_savings:
                cw_saving = D[i,0]+D[0,j]-D[i,j]
                if cw_saving<0.0:
                    break
                
            left_route = endnode_to_route[i]
            right_route = endnode_to_route[j]
            
            # the node is already an internal part of a longer segment
            if ((left_route is None) or
                (right_route is None) or
                (left_route==right_route)):
                continue
            
            if __debug__:
                log(DEBUG-1, "Route #%d : %s"%
                             (left_route, str(routes[left_route])))
                log(DEBUG-1, "Route #%d : %s"%
                             (right_route, str(routes[right_route])))
                
            # check capacity constraint validity
            if C:
                merged_demand = route_demands[left_route]+route_demands[right_route]
                if merged_demand-C_EPS > C:
                    if __debug__:
                        log(DEBUG-1, "Reject merge due to "+
                            "capacity constraint violation")
                    continue
            # if there are route cost constraint, check its validity        
            if L:
                merged_cost = route_costs[left_route]-D[0,i]+\
                                route_costs[right_route]-D[0,j]+\
                                D[i,j]
                if merged_cost-S_EPS > L:
                    if __debug__:
                        log(DEBUG-1, "Reject merge due to "+
                            "maximum route length constraint violation")
                    continue
            
            if trace_graph == True : 
                # Avant la tentative de fusion
                print("Tentative de fusion des itinéraires pour les clients {} et {}".format(i, j))
                for route_index, route in enumerate(routes, start=1):
                    print("Itinéraire avant fusion #{} : {}".format(route_index, route))
        
            # update bookkeeping only on the recieving (left) route
            if C: route_demands[left_route] = merged_demand
            if L: route_costs[left_route] = merged_cost
                
            # merging is done based on the joined endpoints, reverse the 
            #  merged routes as necessary
            if routes[left_route][0]==i:
                routes[left_route].reverse()
            if routes[right_route][-1]==j:
                routes[right_route].reverse()
    
            # the nodes that become midroute points cannot be merged
            if len(routes[left_route])>1:
                endnode_to_route[ routes[left_route][-1] ] = None
            if len(routes[right_route])>1:
                endnode_to_route[ routes[right_route][0] ] = None
            
            # all future references to right_route are to merged route
            endnode_to_route[ routes[right_route][-1] ] = left_route
            
            # merge with list concatenation
            routes[left_route].extend( routes[right_route] )
            routes[right_route] = None
            
            if __debug__:
                dbg_sol = routes2sol(routes)
                log(DEBUG-1, "Merged, resulting solution is %s (%.2f)"%
                             (str(dbg_sol), objf(dbg_sol,D)))
                
            if trace_graph == True :     
                if __debug__:
                    print("Après fusion des itinéraires pour les clients {} et {}".format(i, j))
                    for route_index, route in enumerate(routes, start=1):
                        print("Itinéraire après fusion #{} : {}".format(route_index, route))
                    print("---" * 10)  # Séparateur pour plus de clarté entre les itérations
                    update_plot(routes, coordinates)

    except KeyboardInterrupt: # or SIGINT
        interrupted_sol = routes2sol(routes)
        raise KeyboardInterrupt(interrupted_sol)
        
    return routes2sol(routes)

    
def calculate_tour_cost(matrix, tour):
    total_cost = 0
    for i in range(len(tour) - 1):
        total_cost += matrix[tour[i]][tour[i + 1]]
    return total_cost


    
# =============================================================================
# Data
# ============================================================================

problem = read_TSPLIB_CVRP('Q1.tsp')
distance_matrix = problem.distance_matrix
coordinates= np.array(problem.coordinate_points)
# =============================================================================
# Main
# =============================================================================


route = parallel_savings_init(
    D=distance_matrix, 
    d=problem.customer_demands, 
    C=problem.capacity_constraint, trace_graph= True )

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
print(route)
print(distance)
graph(np.array(problem.coordinate_points),route, distance, nom_algo= 'Clark & Wright')

print(f"Le temps d'exécution total est de {execution_time} secondes.")
print(f"Le temps d'exécution par point est de {time_per_point} secondes par point.")

#%%
