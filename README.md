# Optimisation de Routage de Véhicules et Problème du Voyageur de Commerce

Ce dépôt contient les implémentations et analyses de différents algorithmes d'optimisation pour le problème du voyageur de commerce (TSP) et le problème de routage de véhicules (VRP). Ce travail a été réalisé dans le cadre d'un cours.

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

---

Auteur: Pierre-Adrien Lefèvre