import copy

import numpy.random as rnd

from alns_state.state import CvrpState


class Removal:
    def __init__(self,
                 customers_to_remove = 5,
                 degree = 10):
        self.customers_to_remove = customers_to_remove
        self.degree = degree
    

    def random_removal(self, state: CvrpState, rnd_state: rnd.RandomState):
        """
        Removes a number of randomly selected customers from the passed-in solution.
        """
        destroyed = state.copy()

        for customer in rnd_state.choice(
                range(1, destroyed.data.dimension), self.customers_to_remove, replace=False
        ):
            destroyed.unassigned.append(customer)
            route = destroyed.find_route(customer)
            route.remove(customer)

        return self.remove_empty_routes(destroyed)

    def shaw_removal(self, state: CvrpState, rnd_state: rnd.RandomState):
        q = self.customers_to_remove
        p = self.degree
        destroyed = state.copy()
        
        while q > 0:
            y = rnd_state.random()
            removed_customer = destroyed.data.customers[int(pow(y, p) * len(destroyed.data.customers))]
            if removed_customer in destroyed.unassigned:
                continue
            destroyed = self.remove_specific_customer(destroyed, removed_customer)
            q = q - 1
        
        return self.remove_empty_routes(destroyed)
        

    def remove_empty_routes(self, state: CvrpState):
        """
        Remove empty routes after applying the destroy operator.
        """
        state.routes = [route for route in state.routes if len(route) != 0]
        return state


    def remove_specific_customer(self, state: CvrpState, customer: int):
        destroyed = copy.deepcopy(state)

        destroyed.unassigned.append(customer)
        route = destroyed.find_route(customer)
        route.remove(customer)

        return destroyed


    def sort_desc_cost_request(self, state: CvrpState):
        sorted_cost_idx = list()

        for customer in state.data.customers:
            delta = state.cost - self.remove_specific_customer(state, customer).cost
            sorted_cost_idx.append((customer, delta))

        sorted_cost_idx.sort(key=lambda el: el[1], reverse=True)
        return sorted_cost_idx


    def worst_removal(self, state: CvrpState, rnd_state: rnd.RandomState):
        q = self.customers_to_remove
        p = self.degree
        destroyed = copy.deepcopy(state)
        sorted_cost_customer = self.sort_desc_cost_request(state)
        while q > 0:
            y = rnd_state.random()
            r = sorted_cost_customer[int(pow(y, p) * len(sorted_cost_customer))]
            removed_customer = r[0]
            if removed_customer in destroyed.unassigned:
                continue
            destroyed = self.remove_specific_customer(destroyed, removed_customer)
            q = q - 1
        return self.remove_empty_routes(destroyed)
