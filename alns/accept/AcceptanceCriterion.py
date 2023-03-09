from abc import ABC, abstractmethod

from numpy.random import RandomState

from alns.State import State


class AcceptanceCriterion(ABC):
    """
    Base class describing an acceptance criterion.
    """

    @abstractmethod
    def __call__(
        self, rnd: RandomState, best: State, current: State, candidate: State
    ) -> bool:
        """
        Determines whether to accept the proposed, candidate solution based on
        this acceptance criterion and the other solution states.

        Parameters
        ----------
        rnd
            May be used to draw random numbers from.
        best
            The best solution alns_state observed so far.
        current
            The current solution alns_state.
        candidate
            The proposed solution alns_state.

        Returns
        -------
        bool
            Whether to accept the candidate alns_state (True), or not (False).
        """
        return NotImplemented
