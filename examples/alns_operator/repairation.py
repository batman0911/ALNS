import copy

import numpy.random as rnd

from alns_state.state import CvrpState

class Repairation:
  def __init__(self) -> None:
    pass
  
  def greedy_repair(self, state: CvrpState, rnd_state: rnd.RandomState):
    """
    Inserts the unassigned customers in the best route. If there are no
    feasible insertions, then a new route is created.
    """
    rnd_state.shuffle(state.unassigned)

    while len(state.unassigned) != 0:
        customer = state.unassigned.pop()
        route, idx = self.best_insert(customer, state)

        if route is not None:
            route.insert(idx, customer)
        else:
            state.routes.append([customer])

    return state


  def best_insert(self, customer: int, state: CvrpState):
      """
      Finds the best feasible route and insertion idx for the customer.
      Return (None, None) if no feasible route insertions are found.
      """
      best_cost, best_route, best_idx = None, None, None

      for route in state.routes:
          for idx in range(len(route) + 1):

              if self.can_insert(state, customer, route):
                  cost = self.insert_cost(state, customer, route, idx)

                  if best_cost is None or cost < best_cost:
                      best_cost, best_route, best_idx = cost, route, idx

      return best_route, best_idx


  def can_insert(self, state: CvrpState, customer, route):
      """
      Checks if inserting customer does not exceed vehicle capacity.
      """
      total = sum(state.data.demands[cust] for cust in route) + state.data.demands[customer]
      return total <= state.data.capacity


  def insert_cost(self, state: CvrpState, customer, route, idx):
      """
      Computes the insertion cost for inserting customer in route at idx.
      """
      pred = 0 if idx == 0 else route[idx - 1]
      succ = 0 if idx == len(route) else route[idx]

      # Increase in cost by adding the customer
      cost = state.data.distances[pred][customer] + state.data.distances[customer][succ]

      # Decrease in cost by removing old edge (pred, succ)
      cost -= state.data.distances[pred][succ]

      return cost