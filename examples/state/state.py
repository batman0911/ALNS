import copy

import numpy as np

from alns import State


class CvrpState(State):
    """
    Solution state for CVRP. It has two data members, routes and unassigned.
    Routes is a list of list of integers, where each inner list corresponds to
    a single route denoting the sequence of customers to be visited. A route
    does not contain the start and end depot. Unassigned is a list of integers,
    each integer representing an unassigned customer.
    """

    def __init__(self, data, routes, unassigned=None):
        self.data = data
        self.routes: list = routes
        self.unassigned = unassigned if unassigned is not None else []

    def copy(self):
        return CvrpState(copy.deepcopy(self.routes), self.unassigned.copy())

    def objective(self):
        """
        Computes the total route costs.
        """
        return sum(self.route_cost(route) for route in self.routes)

    @property
    def cost(self):
        """
        Alias for objective method. Used for plotting.
        """
        return self.objective()

    def find_route(self, customer) -> list:
        """
        Return the route that contains the passed-in customer.
        """
        for route in self.routes:
            if customer in route:
                return route

        raise ValueError(f"Solution does not contain customer {customer}.")

    def route_cost(self, route):
        tour = [0] + route + [0]
        return sum(self.data.distances[tour[idx]][tour[idx + 1]] for idx in range(len(tour) - 1))


def neighbors(data, customer):
    """
    Return the nearest neighbors of the customer, excluding the depot.
    """
    locations = np.argsort(data.distances[customer])
    return locations[locations != 0]


def nearest_neighbor(data):
    """
    Build a solution by iteratively constructing routes, where the nearest
    customer is added until the route has met the vehicle capacity limit.
    """
    routes = []
    unvisited = list(range(1, data.dimension))

    while unvisited:
        route = [0]  # Start at the depot
        route_demands = 0

        while unvisited:
            # Add the nearest unvisited customer to the route till max capacity
            current = route[-1]
            nearest = [nb for nb in neighbors(data, current) if nb in unvisited][0]

            if route_demands + data.demands[nearest] > data.capacity:
                break

            route.append(nearest)
            unvisited.remove(nearest)
            route_demands += data.demands[nearest]

        customers = route[1:]  # Remove the depot
        routes.append(customers)

    return CvrpState(data, routes)
