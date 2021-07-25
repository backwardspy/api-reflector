"""
Contains types and methods related to rules engine actions.
"""

from enum import Enum


class Action(Enum):
    """
    Actions are optional extras that can be executed when a certain response is chosen.
    """

    DELAY = "DELAY"

    def __str__(self) -> str:
        return self.value
