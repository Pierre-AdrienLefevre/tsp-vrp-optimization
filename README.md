# Optimisation de Routage de Véhicules et Problème du Voyageur de Commerce
# Vehicle Routing Optimization and Traveling Salesman Problem

<details>
<summary>🇫🇷 Version Française (cliquez pour déplier)</summary>

Ce dépôt contient les implémentations et analyses de différents algorithmes d'optimisation pour le problème du voyageur de commerce (TSP) et le problème de routage de véhicules (VRP). Ce travail a été réalisé dans le cadre du cours SYS817 - Systèmes de distribution et de transport intelligents à l'École de technologie supérieure.

## Organisation du Projet

```
.
├── Q1/                                # Implémentations de base du TSP
│   ├── Clark_and_Wright_Q1.py         # Algorithme de Clark & Wright
│   ├── Double Tree.py                 # Algorithme Double Tree
│   ├── Le plus Rapproché.py           # Algorithme du plus proche voisin
│   ├── Le plus éloigné.py             # Algorithme d'insertion du plus éloigné
│   ├── LireFichierTSP.py              # Utilitaire de lecture de fichiers TSP
│   ├── Minimisé le cout d'insertion.py # Minimisation du coût d'insertion
│   ├── Plus proche voisins Devoir.py  # Variante du plus proche voisin
│   └── creation_graph.py              # Utilitaire de visualisation
│
├── Q2/                                # Heuristiques avancées pour le TSP
│   ├── 2-OPT.py                       # Amélioration locale 2-OPT
│   ├── 3-OPT.py                       # Amélioration locale 3-OPT
│   ├── Clark_and_Wright_Q2.py         # C&W avec améliorations
│   ├── Le_plus_éloigné_Q2.py          # Insertion plus éloignée avec améliorations
│   ├── Plus_proche_voisins_Q2.py      # Plus proche voisin avec améliorations
│   ├── Recruit_Simulé.py              # Recuit simulé
│   ├── Tabu.py                        # Recherche tabou
│   ├── Q2_1.tsp, Q2_2.tsp, Q2_3.tsp   # Instances de test
│   └── pyCombinatorial 11Test.ipynb   # Tests et évaluations
│
├── Q3/                                # Variantes du VRP
│   ├── Modèle CVRPTW.py               # Modèle pour CVRP avec fenêtres temporelles
│   └── model.ilp                      # Modèle de programmation linéaire
│
└── Q4/                                # Métaheuristiques pour CVRP
    ├── ALNS.py                        # Algorithme Adaptive Large Neighborhood Search
    ├── Greedy.py                      # Construction gloutonne
    ├── A-n32-k5.vrp, etc.             # Instances de référence
    └── *.sol                          # Solutions de référence
```

## Implémentations d'Algorithmes

### Question 1: Heuristiques de Base

- **Clark & Wright**: Algorithme d'épargne pour le VRP
- **Plus Proche Voisin**: Construction itérative basée sur la proximité
- **Insertion du Plus Proche**: Insertion en fonction de la proximité
- **Insertion du Plus Éloigné**: Insertion basée sur la distance maximale
- **Minimisation du Coût d'Insertion**: Insertion basée sur le coût minimal
- **Double Tree**: Basé sur un arbre couvrant minimum

### Question 2: Heuristiques Avancées

- **2-OPT**: Amélioration locale par échange de 2 arêtes
- **3-OPT**: Amélioration locale par échange de 3 arêtes
- **Recherche Tabou**: Métaheuristique avec liste tabou
- **Recuit Simulé**: Métaheuristique basée sur le refroidissement

Tests et comparaisons effectués sur des instances de:
- 14 villes
- 150 villes
- 1037 villes

### Question 3: Variantes du VRP

- **CVRPTW**: Problème de tournées de véhicules avec fenêtres temporelles
  - Formulation mathématique
  - Implémentation avec solveur (Gurobi/CPLEX)

### Question 4: Métaheuristiques Avancées

- **ALNS**: Adaptive Large Neighborhood Search
  - Implémentation de base
  - Version améliorée avec Slack Induction by Substring Removal (SISR)
  - Tests sur des instances de 32, 242 et 1001 villes

## Résultats Notables

### Comparaison des Performances (Q1)

| Algorithme | Distance (10 villes) |
|------------|-------------|
| Minimiser le Coût d'Insertion | 139.29 |
| Plus Proche Voisin | 139.59 |
| Insertion la Plus Proche | 140.65 |
| Clark & Wright | 140.37 |
| Insertion la Plus Éloignée | 144.65 |
| Double Tree | 156.88 |

### Performance de l'ALNS (Q4)

| Instance | ALNS Simple | ALNS avec SISR | Optimal | Écart SISR/Optimal |
|----------|-------------|----------------|---------|-------------------|
| 32 villes | 873.88 (+11.5%) | 787.08 | 784 | +0.4% |
| 242 villes | 132156 (+6.8%) | 127459 | 123750 | +3.0% |
| 1001 villes | 83384 (+15%) | 82987 | 72355 | +14.7% |

## Conclusion

Les résultats montrent que:

1. Pour les petites instances, les heuristiques simples comme la minimisation du coût d'insertion et le plus proche voisin offrent une bonne performance.
2. L'ajout d'opérateurs de recherche locale (2-OPT, 3-OPT) améliore significativement les solutions.
3. Pour les grandes instances, les métaheuristiques comme l'ALNS sont efficaces, particulièrement avec des mécanismes avancés comme SISR.
4. La performance des algorithmes diminue avec l'augmentation de la taille du problème, suggérant la nécessité d'ajustements spécifiques pour les grands jeux de données.

## Références

- [1] OpenAI. (2024). ChatGPT : OpenAI ChatGPT model documentation.
- [2] Ruthmair, M. (2024). VRP GitHub Repository.
- [3] Wouda, N. (2024). ALNS GitHub Repository : Capacitated Vehicle Routing Problem Example.

</details>

<details>
<summary>🇬🇧 English Version (click to expand)</summary>

This repository contains implementations and analyses of various optimization algorithms for the Traveling Salesman Problem (TSP) and Vehicle Routing Problem (VRP). This work was carried out as part of the SYS817 - Intelligent Distribution and Transportation Systems course at École de technologie supérieure.

## Project Organization

```
.
├── Q1/                                # Basic TSP implementations
│   ├── Clark_and_Wright_Q1.py         # Clark & Wright algorithm
│   ├── Double Tree.py                 # Double Tree algorithm
│   ├── Le plus Rapproché.py           # Nearest neighbor algorithm
│   ├── Le plus éloigné.py             # Farthest insertion algorithm
│   ├── LireFichierTSP.py              # TSP file reader utility
│   ├── Minimisé le cout d'insertion.py # Minimum insertion cost
│   ├── Plus proche voisins Devoir.py  # Nearest neighbor variant
│   └── creation_graph.py              # Visualization utility
│
├── Q2/                                # Advanced TSP heuristics
│   ├── 2-OPT.py                       # 2-OPT local improvement
│   ├── 3-OPT.py                       # 3-OPT local improvement
│   ├── Clark_and_Wright_Q2.py         # C&W with improvements
│   ├── Le_plus_éloigné_Q2.py          # Improved farthest insertion
│   ├── Plus_proche_voisins_Q2.py      # Improved nearest neighbor
│   ├── Recruit_Simulé.py              # Simulated annealing
│   ├── Tabu.py                        # Tabu search
│   ├── Q2_1.tsp, Q2_2.tsp, Q2_3.tsp   # Test instances
│   └── pyCombinatorial 11Test.ipynb   # Tests and evaluations
│
├── Q3/                                # VRP variants
│   ├── Modèle CVRPTW.py               # CVRP with time windows model
│   └── model.ilp                      # Linear programming model
│
└── Q4/                                # Metaheuristics for CVRP
    ├── ALNS.py                        # Adaptive Large Neighborhood Search
    ├── Greedy.py                      # Greedy construction
    ├── A-n32-k5.vrp, etc.             # Reference instances
    └── *.sol                          # Reference solutions
```

## Algorithm Implementations

### Question 1: Basic Heuristics

- **Clark & Wright**: Savings algorithm for VRP
- **Nearest Neighbor**: Iterative construction based on proximity
- **Nearest Insertion**: Insertion based on proximity
- **Farthest Insertion**: Insertion based on maximum distance
- **Minimum Insertion Cost**: Insertion based on minimum cost
- **Double Tree**: Based on minimum spanning tree

### Question 2: Advanced Heuristics

- **2-OPT**: Local improvement by exchanging 2 edges
- **3-OPT**: Local improvement by exchanging 3 edges
- **Tabu Search**: Metaheuristic with tabu list
- **Simulated Annealing**: Metaheuristic based on cooling process

Tests and comparisons performed on instances of:
- 14 cities
- 150 cities
- 1037 cities

### Question 3: VRP Variants

- **CVRPTW**: Capacitated Vehicle Routing Problem with Time Windows
  - Mathematical formulation
  - Implementation with solver (Gurobi/CPLEX)

### Question 4: Advanced Metaheuristics

- **ALNS**: Adaptive Large Neighborhood Search
  - Basic implementation
  - Improved version with Slack Induction by Substring Removal (SISR)
  - Tests on instances of 32, 242, and 1001 cities

## Notable Results

### Performance Comparison (Q1)

| Algorithm | Distance (10 cities) |
|-----------|-------------|
| Minimum Insertion Cost | 139.29 |
| Nearest Neighbor | 139.59 |
| Nearest Insertion | 140.65 |
| Clark & Wright | 140.37 |
| Farthest Insertion | 144.65 |
| Double Tree | 156.88 |

### ALNS Performance (Q4)

| Instance | Simple ALNS | ALNS with SISR | Optimal | Gap SISR/Optimal |
|----------|-------------|----------------|---------|-------------------|
| 32 cities | 873.88 (+11.5%) | 787.08 | 784 | +0.4% |
| 242 cities | 132156 (+6.8%) | 127459 | 123750 | +3.0% |
| 1001 cities | 83384 (+15%) | 82987 | 72355 | +14.7% |

## Conclusion

The results show that:

1. For small instances, simple heuristics like minimum insertion cost and nearest neighbor offer good performance.
2. Adding local search operators (2-OPT, 3-OPT) significantly improves solutions.
3. For large instances, metaheuristics like ALNS are effective, particularly with advanced mechanisms like SISR.
4. The performance of algorithms decreases as problem size increases, suggesting the need for specific adjustments for large datasets.

## References

- [1] OpenAI. (2024). ChatGPT: OpenAI ChatGPT model documentation.
- [2] Ruthmair, M. (2024). VRP GitHub Repository.
- [3] Wouda, N. (2024). ALNS GitHub Repository: Capacitated Vehicle Routing Problem Example.

</details>

---

**Auteur/Author**: Pierre-Adrien Lefèvre  
**Licence/License**: [MIT](LICENSE.md)