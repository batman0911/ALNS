import numpy.random as rnd

from examples.state.state import CvrpState

customers_to_remove = 5


def random_removal(state: CvrpState, rnd_state: rnd.RandomState):
    """
    Removes a number of randomly selected customers from the passed-in solution.
    """
    destroyed = state.copy()

    for customer in rnd_state.choice(
            range(1, state.data.dimension), customers_to_remove, replace=False
    ):
        destroyed.unassigned.append(customer)
        route = destroyed.find_route(customer)
        route.remove(customer)

    return remove_empty_routes(destroyed)


def remove_empty_routes(state: CvrpState):
    """
    Remove empty routes after applying the destroy operator.
    """
    state.routes = [route for route in state.routes if len(route) != 0]
    return state


def remove_specific_customer(state: CvrpState, customer: int):
    destroyed = state.copy()

    destroyed.unassigned.append(customer)
    route = destroyed.find_route(customer)
    route.remove(customer)

    return remove_empty_routes(destroyed)


def sort_desc_cost_request(state: CvrpState):
    sorted_cost_idx = []
    for customer in state.data.customers:
        print(customer)
    return None


q = 5


def worst_removal(state: CvrpState, rnd_state: rnd.RandomState):
    global q
    destroyed = state.copy()
    # calculate cost if remove i
    # for customer in
