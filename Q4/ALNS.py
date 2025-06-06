# -*- coding: utf-8 -*-
"""Capacitated VRP notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VKqyl2A2-TFkT9RE1TQG8BUufxFOdEZB
"""

import copy
from types import SimpleNamespace

import vrplib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd

from alns import ALNS
from alns.accept import RecordToRecordTravel
from alns.select import RouletteWheel
from alns.stop import MaxRuntime

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

SEED = 1234

"""# The capacitated vehicle routing problem
The vehicle routing problem (VRP) is one of the most studied problems in operations research. Given a fleet of vehicles and customers, the goal is to construct a set of routes such that each customer is visited exactly once, while minimizing the total distance traveled by the vehicles.

Despite decades of research, the VRP (and variants thereof) remains a very hard problem to solve and new algorithms continue to be developed to address this problem. A related and interesting fact is that ALNS was originally proposed by [Ropke and Pisinger (2006)](https://pubsonline.informs.org/doi/abs/10.1287/trsc.1050.0135?casa_token=-DeLGU-Nr_4AAAAA:hTPxhhAn8TRi5h8p5LdQ_r-tQ1j4lCD4-K4ZR4gSi0e9O6reL6vcyfC0NZmkW1hoQGkUEjcumwH6) to solve many variants of the vehicle routing problem.

In this notebook, we use ALNS to solve the most famous VRP variant: the *Capacitated Vehicle Routing Problem (CVRP)*. The CVRP can be described using an undirected graph $G=(V,E)$, where $V$ is the vertex set and $E$ is the edge set. The vertex set $V$ is partitioned into $V=\{0\} \cup V_c$, where $0$ is the depot and $V_c=\{1, \dots, n\}$ denotes the set of $n$ customers. Each customer $i \in V_c$ has a demand $q_i > 0$. A distance $d_{ij}$ is associated with each edge $(i, j) \in E$. We assume that we have an unlimited fleet of homogeneous vehicles with capacity $Q$ located at the depot. A feasible solution to the CVRP is a set of routes, each served by a single vehicle, such that each customer is served exactly once and none of the routes exceed the vehicle capacity. The goal is to minimize the total distance traveled.

## Data
[CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/) contains a large collection of CVRP benchmark instances. The library is actively maintained and new best known solutions are updated regularly. We use the `vrplib` package to read the `ORTEC-n242-k12` instance, which consists of 241 customers (+ 1 depot) and 12 vehicles, but we assume that an unlimited number of vehicles is available.
"""


# 32 Points : 
data = vrplib.read_instance('A-n32-k5.vrp')
bks = SimpleNamespace(**vrplib.read_solution('A-n32-k5.sol'))

'''
# 242 Points : 
data = vrplib.read_instance('ORTEC-n242-k12.vrp')
bks = SimpleNamespace(**vrplib.read_solution('ORTEC-n242-k12.sol'))
'''
# 1001 Points : 
data = vrplib.read_instance('X-n1001-k43.vrp')
bks = SimpleNamespace(**vrplib.read_solution('X-n1001-k43.sol'))



"""The `bks` variable contains the best known solution. Let's plot it, together with the coordinates of the customers:"""

def plot_solution(solution, name="CVRP solution"):
    """
    Plot the routes of the passed-in solution.
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    cmap = matplotlib.cm.rainbow(np.linspace(0, 1, len(solution.routes)))

    for idx, route in enumerate(solution.routes):
        ax.plot(
            [data["node_coord"][loc][0] for loc in [0] + route + [0]],
            [data["node_coord"][loc][1] for loc in [0] + route + [0]],
            color=cmap[idx],
            marker='.'
        )

    # Plot the depot
    kwargs = dict(label="Depot", zorder=3, marker="*", s=750)
    ax.scatter(*data["node_coord"][0], c="tab:red", **kwargs)

    ax.set_title(f"{name}\n Total distance: {solution.cost}")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.legend(frameon=False, ncol=3)

plot_solution(bks, name="Best known solution")
plt.show()

"""## Solution state"""

class CvrpState:
    """
    Solution state for CVRP. It has two data members, routes and unassigned.
    Routes is a list of list of integers, where each inner list corresponds to
    a single route denoting the sequence of customers to be visited. A route
    does not contain the start and end depot. Unassigned is a list of integers,
    each integer representing an unassigned customer.
    """

    def __init__(self, routes, unassigned=None):
        self.routes = routes
        self.unassigned = unassigned if unassigned is not None else []

    def copy(self):
        return CvrpState(copy.deepcopy(self.routes), self.unassigned.copy())

    def objective(self):
        """
        Computes the total route costs.
        """
        return sum(route_cost(route) for route in self.routes)

    @property
    def cost(self):
        """
        Alias for objective method. Used for plotting.
        """
        return self.objective()

    def find_route(self, customer):
        """
        Return the route that contains the passed-in customer.
        """
        for route in self.routes:
            if customer in route:
                return route

        raise ValueError(f"Solution does not contain customer {customer}.")

def route_cost(route):
    distances = data["edge_weight"]
    tour = [0] + route + [0]

    return sum(distances[tour[idx]][tour[idx + 1]]
               for idx in range(len(tour) - 1))

"""## Destroy operators

Destroy operators break parts of a solution down, leaving an incomplete state. This is the first part of each iteration of the ALNS meta-heuristic; the incomplete solution is subsequently repaired by any one repair operator. We will consider one destroy operator: **random removal**. We will also use a separate parameter, the degree of destruction, to control the extent of the damage done to a solution in each step.
"""

degree_of_destruction = 0.05
customers_to_remove = int((data["dimension"] - 1) * degree_of_destruction)

def random_removal(state, rnd_state):
    """
    Removes a number of randomly selected customers from the passed-in solution.
    """
    destroyed = state.copy()

    for customer in rnd_state.choice(
        range(1, data["dimension"]), customers_to_remove, replace=False
    ):
        destroyed.unassigned.append(customer)
        route = destroyed.find_route(customer)
        route.remove(customer)

    return remove_empty_routes(destroyed)


def remove_empty_routes(state):
    """
    Remove empty routes after applying the destroy operator.
    """
    state.routes = [route for route in state.routes if len(route) != 0]
    return state

"""## Repair operators
We implement a simple, **greedy repair** strategy. It iterates over the set of unassigned customers and finds the best route and index to insert to, i.e., with the least increase in cost.
"""

def greedy_repair(state, rnd_state):
    """
    Inserts the unassigned customers in the best route. If there are no
    feasible insertions, then a new route is created.
    """
    rnd_state.shuffle(state.unassigned)

    while len(state.unassigned) != 0:
        customer = state.unassigned.pop()
        route, idx = best_insert(customer, state)

        if route is not None:
            route.insert(idx, customer)
        else:
            state.routes.append([customer])

    return state


def best_insert(customer, state):
    """
    Finds the best feasible route and insertion idx for the customer.
    Return (None, None) if no feasible route insertions are found.
    """
    best_cost, best_route, best_idx = None, None, None

    for route in state.routes:
        for idx in range(len(route) + 1):

            if can_insert(customer, route):
                cost = insert_cost(customer, route, idx)

                if best_cost is None or cost < best_cost:
                    best_cost, best_route, best_idx = cost, route, idx

    return best_route, best_idx


def can_insert(customer, route):
    """
    Checks if inserting customer does not exceed vehicle capacity.
    """
    total = data["demand"][route].sum() + data["demand"][customer]
    return total <= data["capacity"]


def insert_cost(customer, route, idx):
    """
    Computes the insertion cost for inserting customer in route at idx.
    """
    dist = data["edge_weight"]
    pred = 0 if idx == 0 else route[idx - 1]
    succ = 0 if idx == len(route) else route[idx]

    # Increase in cost of adding customer, minus cost of removing old edge
    return dist[pred][customer] + dist[customer][succ] - dist[pred][succ]

"""## Initial solution
We need an initial solution that is going to be destroyed and repaired by the ALNS heuristic. To this end, we use a simple *nearest neighbor (NN)* heuristic. NN starts with an empty solution and iteratively adds the nearest customer to the routes. If there are no routes available, then a new route is created.
"""

def neighbors(customer):
    """
    Return the nearest neighbors of the customer, excluding the depot.
    """
    locations = np.argsort(data["edge_weight"][customer])
    return locations[locations != 0]


def nearest_neighbor():
    """
    Build a solution by iteratively constructing routes, where the nearest
    customer is added until the route has met the vehicle capacity limit.
    """
    routes = []
    unvisited = set(range(1, data["dimension"]))

    while unvisited:
        route = [0]  # Start at the depot
        route_demands = 0

        while unvisited:
            # Add the nearest unvisited customer to the route till max capacity
            current = route[-1]
            nearest = [nb for nb in neighbors(current) if nb in unvisited][0]

            if route_demands + data["demand"][nearest] > data["capacity"]:
                break

            route.append(nearest)
            unvisited.remove(nearest)
            route_demands += data["demand"][nearest]

        customers = route[1:]  # Remove the depot
        routes.append(customers)

    return CvrpState(routes)

plot_solution(nearest_neighbor(), 'Nearest neighbor solution')
plt.show()

"""## Heuristic solution

Let's now construct our ALNS heuristic. Since we only have one destroy and repair operator, we do not actually use any adaptive operator selection -- but you can easily add more destroy and repair operators.
"""

alns = ALNS(rnd.RandomState(SEED))

alns.add_destroy_operator(random_removal)

alns.add_repair_operator(greedy_repair)

init = nearest_neighbor()
select = RouletteWheel([25, 5, 1, 0], 0.8, 1, 1)
accept = RecordToRecordTravel.autofit(init.objective(), 0.02, 0, 9000)
stop = MaxRuntime(600)

result = alns.iterate(init, select, accept, stop)

solution = result.best_state
objective = solution.objective()
pct_diff = 100 * (objective - bks.cost) / bks.cost

print(f"Best heuristic objective is {objective}.")
print(f"This is {pct_diff:.1f}% worse than the optimal solution, which is {bks.cost}.")

_, ax = plt.subplots(figsize=(12, 6))
result.plot_objectives(ax=ax)
plt.show()

"""Let's have a look at the solution:"""

plot_solution(solution, 'Simple ALNS')
plt.show()
"""## Slack-induced substring removal
The simple destroy and repair operator from above work fine, but there are better destroy and repair operators for CVRP. One example is the *Slack Induction by Substring Removal (SISR)* method proposed by [Christiaens and Vanden Berghe (2020)](https://pubsonline.informs.org/doi/abs/10.1287/trsc.2019.0914?casa_token=lPUXU1Ax8PIAAAAA:yTE9Pu6L9QGPRu_vt-ZMHF0AZvL9gV0fNS4QAUTOJboQcgTVyOR9_RTbm9rZcImyKI4GUW9pLv1j). SISR obtains state-of-the-art results using a destroy operator that, instead of removing random customers, removes partial routes (called *strings*) that are all located near each other. Moreover, a blinking feature is added to the greedy repair operator, where certain insertion checks are skipped. For more details, we refer to the paper.

In the following, we will implement a simplified version of the string removal operator and replace the random destroy operator.
"""

MAX_STRING_REMOVALS = 2
MAX_STRING_SIZE = 12

def string_removal(state, rnd_state):
    """
    Remove partial routes around a randomly chosen customer.
    """
    destroyed = state.copy()

    avg_route_size = int(np.mean([len(route) for route in state.routes]))
    max_string_size = max(MAX_STRING_SIZE, avg_route_size)
    max_string_removals = min(len(state.routes), MAX_STRING_REMOVALS)

    destroyed_routes = []
    center = rnd_state.randint(1, data["dimension"])

    for customer in neighbors(center):
        if len(destroyed_routes) >= max_string_removals:
            break

        if customer in destroyed.unassigned:
            continue

        route = destroyed.find_route(customer)
        if route in destroyed_routes:
            continue

        customers = remove_string(route, customer, max_string_size, rnd_state)
        destroyed.unassigned.extend(customers)
        destroyed_routes.append(route)

    return destroyed


def remove_string(route, cust, max_string_size, rnd_state):
    """
    Remove a string that constains the passed-in customer.
    """
    # Find consecutive indices to remove that contain the customer
    size = rnd_state.randint(1, min(len(route), max_string_size) + 1)
    start = route.index(cust) - rnd_state.randint(size)
    idcs = [idx % len(route) for idx in range(start, start + size)]

    # Remove indices in descending order
    removed_customers = []
    for idx in sorted(idcs, reverse=True):
        removed_customers.append(route.pop(idx))

    return removed_customers

alns = ALNS(rnd.RandomState(SEED))

alns.add_destroy_operator(string_removal)

alns.add_repair_operator(greedy_repair)

init = nearest_neighbor()
select = RouletteWheel([25, 5, 1, 0], 0.8, 1, 1)
accept = RecordToRecordTravel.autofit(init.objective(), 0.02, 0, 6000)
stop = MaxRuntime(600)

result = alns.iterate(init, select, accept, stop)

_, ax = plt.subplots(figsize=(12, 6))
result.plot_objectives(ax=ax)

solution = result.best_state
objective = solution.objective()
pct_diff = 100 * (objective - bks.cost) / bks.cost

print(f"Best heuristic objective is {objective}.")
print(f"This is {pct_diff:.1f}% worse than the optimal solution, which is {bks.cost}.")
plot_solution(solution, 'String removals')
plt.show()

"""## Conclusions

In this notebook we implemented two heuristics for the CVRP, using the ALNS meta-heuristic framework. The first heuristic used a random customer destroy operator and we obtained a solution which is 6.8% worse than the best known solution. The second heuristic used a destroy operator which removes strings arround a randomly selected customer and we obtained a solution that is only 3% worse than the best known solution.

This example shows that by constructing problem-specific operators, one can create even more powerful ALNS heuristics.
"""

