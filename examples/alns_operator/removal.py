import copy

import numpy.random as rnd

from alns_state.state import CvrpState

customers_to_remove = 5


def random_removal(state: CvrpState, rnd_state: rnd.RandomState):
    """
    Removes a number of randomly selected customers from the passed-in solution.
    """
    # destroyed = alns_state.copy()

    for customer in rnd_state.choice(
            range(1, state.data.dimension), customers_to_remove, replace=False
    ):
        state.unassigned.append(customer)
        route = state.find_route(customer)
        route.remove(customer)

    return remove_empty_routes(state)


def remove_empty_routes(state: CvrpState):
    """
    Remove empty routes after applying the destroy operator.
    """
    state.routes = [route for route in state.routes if len(route) != 0]
    return state


def remove_specific_customer(state: CvrpState, customer: int):
    destroyed = copy.deepcopy(state)

    destroyed.unassigned.append(customer)
    route = destroyed.find_route(customer)
    route.remove(customer)

    return remove_empty_routes(destroyed)


def condition(el):
    return el['delta_cost']


def sort_desc_cost_request(state: CvrpState):
    sorted_cost_idx = list()

    for customer in state.data.customers:
        delta = state.cost - remove_specific_customer(state, customer).cost
        sorted_cost_idx.append((customer, delta))

    sorted_cost_idx.sort(key=lambda el: el[1], reverse=True)
    return sorted_cost_idx


def worst_removal(state: CvrpState, rnd_state: rnd.RandomState):
    q = customers_to_remove
    p = 1
    destroyed = copy.deepcopy(state)
    while q > 0:
        sorted_cost_customer = sort_desc_cost_request(destroyed)
        y = rnd_state.random()
        r = sorted_cost_customer[int(pow(y, p) * len(sorted_cost_customer))]
        removed_customer = r[0]
        remove_specific_customer(destroyed, removed_customer)
        q = q - 1
    return destroyed
