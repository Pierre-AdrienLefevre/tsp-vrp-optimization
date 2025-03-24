"""
Created on Sat Feb 10 12:03:28 2024

@author: pierreadrienlefevre
"""

import numpy as np
from LireFichierTSP import read_TSPLIB_CVRP
import time
from creation_graph import graph

# Enregistrer le temps de début
start_time = time.time()

# Fonction pour effectuer un échange 2-opt sur le tour
def calculate_total_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i], tour[i+1]]
    total_distance += distance_matrix[tour[-1], tour[0]]
    return total_distance

def three_opt_swap(tour, distance_matrix, i, j, k):
    """Retourne le meilleur tour obtenu par un échange 3-opt parmi les indices i, j, k."""
    # Meilleur tour et distance trouvés jusqu'à présent
    best_tour = tour
    best_distance = calculate_total_distance(tour, distance_matrix)

    # Générer et tester tous les réarrangements possibles
    possibilities = [
        tour[:i] + tour[i:j][::-1] + tour[j:k][::-1] + tour[k:],  # cas 1
        tour[:i] + tour[j:k] + tour[i:j] + tour[k:],              # cas 2
        tour[:i] + tour[j:k] + tour[i:j][::-1] + tour[k:],        # cas 3
        tour[:i] + tour[j:k][::-1] + tour[i:j] + tour[k:],        # cas 4
        tour[:i] + tour[i:j] + tour[j:k] + tour[k:],              # cas 5 (identique au tour original, inclus pour complétude)
        tour[:i] + tour[j:k][::-1] + tour[i:j][::-1] + tour[k:],  # cas 6
        tour[:i] + tour[k-1:j-1:-1] + tour[i:j] + tour[k:],       # cas 7
        tour[:i] + tour[j-1:i-1:-1] + tour[k-1:j-1:-1] + tour[k:] # cas 8
    ]

    for possibility in possibilities:
        current_distance = calculate_total_distance(possibility, distance_matrix)
        if current_distance < best_distance:
            best_tour = possibility
            best_distance = current_distance

    return best_tour


def three_opt(tour_initial, distance_matrix,temps_max, trace_graph=False):
    amelioration = True
    iteration = 0
    should_break = False  # Flag pour indiquer la sortie anticipée due au temps

    while amelioration and not should_break:  # Vérifier le flag ici
        amelioration = False
        best_distance = calculate_total_distance(tour_initial, distance_matrix)
        best_i, best_j, best_k = None, None, None

        for i in range(1, len(tour_initial) - 2):
            if should_break: break  # Vérifier le flag à chaque niveau de boucle
            for j in range(i + 1, len(tour_initial) - 1):
                if should_break: break  # Vérifier le flag
                for k in range(j + 1, len(tour_initial)):
                    current_time = time.time()
                    if (current_time - start_time) > temps_max:
                        print("Temps d'exécution maximum atteint, arrêt de l'optimisation.")
                        should_break = True  # Mettre à jour le flag
                        break  # Sortie de la boucle interne

                    new_tour = three_opt_swap(tour_initial, distance_matrix, i, j, k)
                    new_distance = calculate_total_distance(new_tour, distance_matrix)

                    if new_distance < best_distance:
                        best_distance = new_distance
                        best_i, best_j, best_k = i, j, k
                        amelioration = True
                        
                        print(f"Iteration {iteration + 1}: Amélioration trouvée: distance = {best_distance:.2f}")
                        if trace_graph:
                            graph(np.array(problem.coordinate_points), new_tour, best_distance, iteration+1, nom_algo='3-OPT')

        if amelioration and not should_break:  # Vérifier le flag avant de faire le swap
            tour_initial = three_opt_swap(tour_initial, distance_matrix, best_i, best_j, best_k)
            iteration += 1

    return tour_initial, best_distance

# =============================================================================
# Data
# ============================================================================

problem = read_TSPLIB_CVRP('Q2_3.tsp')
distance_matrix = problem.distance_matrix
coordinates= np.array(problem.coordinate_points)
temps_max =600
# =============================================================================
# Main
# =============================================================================

tour_initial = [1, 11, 24, 17, 14, 8, 18, 22, 16, 13, 26, 33, 40, 32, 42, 98, 114, 107, 80, 39, 64, 61, 79, 100, 119, 89, 115, 125, 172, 175, 191, 165, 145, 129, 153, 152, 164, 185, 194, 179, 206, 264, 293, 247, 237, 211, 224, 239, 252, 265, 299, 311, 317, 318, 337, 308, 325, 356, 362, 363, 375, 364, 381, 414, 416, 402, 418, 405, 431, 423, 383, 401, 369, 404, 415, 413, 374, 328, 338, 341, 283, 261, 296, 286, 257, 251, 244, 225, 204, 197, 223, 201, 176, 141, 147, 157, 159, 128, 112, 126, 97, 88, 74, 84, 104, 86, 78, 63, 54, 37, 5, 4, 9, 21, 35, 51, 43, 83, 93, 75, 50, 59, 49, 73, 77, 96, 111, 135, 138, 122, 136, 150, 166, 198, 213, 260, 245, 243, 230, 226, 189, 203, 173, 184, 148, 143, 162, 144, 132, 171, 222, 229, 241, 208, 235, 233, 272, 292, 323, 336, 279, 268, 278, 313, 349, 428, 372, 422, 409, 367, 361, 332, 307, 350, 321, 316, 290, 284, 269, 285, 250, 256, 273, 295, 310, 351, 345, 355, 378, 384, 398, 403, 425, 407, 391, 417, 433, 475, 505, 504, 519, 553, 557, 570, 593, 597, 616, 649, 630, 640, 619, 600, 579, 611, 592, 586, 572, 555, 542, 536, 499, 460, 454, 445, 458, 440, 467, 461, 479, 478, 507, 516, 534, 543, 537, 531, 546, 567, 581, 596, 605, 609, 634, 602, 599, 594, 644, 628, 583, 492, 501, 506, 480, 452, 472, 493, 470, 500, 487, 484, 468, 464, 432, 465, 459, 462, 474, 488, 510, 514, 490, 509, 576, 568, 574, 569, 535, 529, 508, 489, 527, 513, 483, 520, 524, 528, 550, 556, 560, 566, 587, 585, 601, 590, 614, 612, 647, 662, 625, 638, 617, 637, 606, 639, 613, 610, 603, 633, 652, 668, 656, 682, 687, 706, 728, 721, 695, 664, 669, 678, 715, 740, 727, 750, 799, 797, 783, 735, 752, 788, 805, 798, 843, 851, 835, 856, 847, 823, 832, 825, 796, 806, 786, 753, 734, 764, 779, 749, 771, 736, 723, 710, 697, 719, 672, 692, 712, 729, 694, 661, 643, 641, 659, 675, 673, 709, 700, 714, 744, 765, 767, 746, 781, 794, 816, 824, 842, 872, 887, 876, 891, 909, 912, 929, 945, 930, 961, 948, 931, 965, 987, 985, 977, 997, 994, 1018, 995, 1016, 1026, 1029, 1009, 999, 968, 981, 962, 991, 967, 973, 976, 953, 939, 936, 926, 905, 880, 915, 937, 946, 963, 971, 966, 969, 944, 925, 916, 901, 884, 892, 840, 852, 854, 850, 862, 871, 882, 896, 890, 917, 919, 933, 949, 972, 938, 940, 952, 980, 1002, 986, 1004, 1006, 1037, 1035, 1023, 1025, 1007, 1013, 1020, 992, 988, 974, 958, 941, 934, 947, 964, 979, 998, 1011, 1015, 1032, 1030, 1033, 1028, 1024, 1022, 1012, 984, 996, 990, 978, 956, 943, 908, 920, 928, 900, 893, 873, 867, 861, 864, 863, 877, 883, 904, 927, 924, 906, 911, 899, 895, 865, 860, 833, 813, 828, 837, 808, 820, 751, 756, 776, 791, 777, 778, 754, 757, 742, 720, 716, 696, 726, 681, 688, 654, 670, 648, 631, 636, 607, 650, 588, 622, 674, 676, 703, 685, 663, 683, 689, 724, 705, 711, 730, 755, 760, 770, 780, 787, 795, 802, 809, 826, 815, 836, 858, 814, 811, 785, 807, 821, 848, 841, 831, 830, 822, 789, 774, 761, 758, 759, 733, 738, 704, 701, 679, 666, 693, 702, 725, 762, 775, 803, 769, 745, 691, 708, 698, 658, 626, 653, 651, 665, 686, 660, 718, 737, 717, 722, 743, 766, 772, 792, 827, 849, 844, 829, 817, 810, 834, 857, 866, 875, 889, 932, 907, 921, 910, 881, 838, 845, 902, 868, 855, 874, 878, 918, 885, 888, 894, 914, 922, 954, 983, 982, 1000, 957, 970, 950, 951, 1019, 1036, 1014, 1005, 1001, 975, 959, 989, 1010, 1017, 1031, 1027, 1003, 1034, 1021, 1008, 993, 955, 960, 942, 923, 886, 897, 935, 898, 879, 913, 903, 869, 846, 819, 801, 763, 793, 790, 812, 839, 870, 859, 853, 818, 784, 773, 768, 748, 731, 699, 713, 677, 680, 684, 707, 732, 741, 782, 800, 804, 747, 739, 690, 671, 655, 629, 627, 595, 582, 645, 667, 632, 623, 584, 580, 559, 549, 545, 522, 521, 497, 498, 427, 438, 496, 466, 457, 495, 530, 547, 541, 558, 563, 608, 620, 621, 577, 552, 551, 532, 540, 494, 503, 449, 456, 442, 400, 343, 289, 303, 306, 360, 411, 334, 298, 242, 236, 220, 202, 181, 178, 174, 215, 219, 232, 207, 199, 168, 169, 123, 140, 134, 108, 62, 27, 12, 7, 29, 41, 48, 47, 72, 20, 15, 34, 57, 71, 94, 113, 116, 76, 58, 56, 99, 117, 121, 82, 90, 120, 130, 158, 155, 151, 180, 196, 212, 218, 227, 280, 259, 254, 190, 187, 154, 163, 238, 263, 301, 276, 304, 319, 342, 352, 274, 275, 288, 281, 302, 305, 348, 335, 339, 353, 373, 390, 386, 387, 406, 437, 450, 443, 436, 420, 376, 380, 393, 379, 444, 463, 477, 481, 482, 515, 526, 548, 575, 573, 591, 604, 615, 635, 642, 657, 646, 618, 624, 598, 571, 564, 589, 565, 523, 539, 485, 448, 441, 447, 455, 502, 517, 533, 518, 525, 554, 561, 578, 562, 544, 491, 511, 538, 512, 486, 473, 469, 476, 435, 471, 446, 424, 394, 395, 396, 377, 397, 408, 389, 371, 359, 365, 347, 333, 312, 320, 309, 294, 300, 331, 315, 324, 340, 368, 370, 430, 426, 412, 388, 354, 327, 291, 277, 249, 262, 314, 330, 358, 392, 421, 439, 429, 451, 453, 434, 419, 382, 385, 410, 399, 366, 357, 322, 326, 344, 346, 329, 287, 282, 248, 266, 267, 253, 258, 234, 186, 160, 214, 221, 193, 170, 146, 131, 118, 124, 167, 192, 216, 210, 188, 142, 133, 127, 149, 161, 182, 228, 209, 240, 246, 297, 271, 270, 255, 217, 205, 183, 195, 231, 200, 177, 156, 139, 137, 106, 92, 103, 95, 110, 109, 65, 60, 87, 105, 102, 91, 81, 53, 44, 69, 85, 101, 66, 55, 36, 23, 10, 38, 52, 70, 68, 46, 67, 45, 28, 30, 31, 25, 19, 3, 2, 6, 1]
tour_initial = [x - 1 for x in tour_initial]



route, distance = three_opt(tour_initial, distance_matrix,temps_max)



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
graph(np.array(problem.coordinate_points),route, distance, nom_algo= '3-OPT')

print(f"Le temps d'exécution total est de {execution_time} secondes.")
print(f"Le temps d'exécution par point est de {time_per_point} secondes par point.")

#%%
