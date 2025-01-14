from abc import ABC, abstractmethod

from numpy.random import RandomState

from alns.State import State


class StoppingCriterion(ABC):
    """
    Base class describing a stopping criterion.
    """

    @abstractmethod
    def __call__(self, rnd: RandomState, best: State, current: State) -> bool:
        """
        Determines whether to stop.

        Parameters
        ----------
        rnd
            May be used to draw random numbers from.
        best
            The best solution alns_state observed so far.
        current
            The current solution alns_state.

        Returns
        -------
        bool
            Whether to stop iterating (True), or not (False).
        """
        return NotImplemented
