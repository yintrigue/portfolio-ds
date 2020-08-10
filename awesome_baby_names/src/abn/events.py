"""The event module contains all the events broadcasted between components in
the AwesomeBabyNames app.
"""

from collections import namedtuple
from abn import constants, constants as ct
from typing import List, Tuple


class BabyInput:
    """BabyInput stores/manages/parses all the user inputs required for the
    analysis rendering.
    """

    def __init__(self) -> None:
        self.__name = ""
        self.__states = []
        self.__gender = ct.GENDER.UKNOWN
        self.__years = namedtuple("Years", ("start", "end"))

    @property
    def name(self) -> str:
        """Name of the baby.
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Name of the baby.
        """
        self.__name = name

    @property
    def states(self) -> Tuple[str]:
        """States to be included for the analysis.
        """
        return self.__states

    @states.setter
    def states(self, states: Tuple[str]) -> None:
        """States to be included for the analysis.
        """
        self.__states = states

    @property
    def gender(self) -> "abn.constants.GENDER":
        """Gender of the baby.
        """
        return self.__gender

    @gender.setter
    def gender(self, gender: "abn.constants.GENDER") -> None:
        """Gender of the baby.
        """
        self.__gender = gender
