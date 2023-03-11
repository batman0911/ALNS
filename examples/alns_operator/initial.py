
import numpy as np
from alns_state.state import CvrpState

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