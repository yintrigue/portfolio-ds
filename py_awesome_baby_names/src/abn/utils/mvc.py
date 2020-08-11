"""MVC framework, implemented using the following references:
    https://tinyurl.com/rt5wd4g
    https://www.guru99.com/mvc-tutorial.html
"""

from abc import ABC,abstractmethod
from typing import List


class Model(ABC):
    """Model for the MVC framework.
    """

    def __init__(self) -> None:
        # ListView
        self.__observers = []

    def add_observer(self, observer: 'View') -> None:
        """Add one observer to observe the model. All observers are required to
        implement the mehod, update(), as the event handler.

        Args:
            observer (View): Observer to be added to listen to the model.
        """
        if isinstance(observer, View):
            self.__observers.append(observer)

    def add_observers(self, observers: List['View']) -> None:
        """Add more than one observers to observe the model. All observers are
        required to implement the mehod, update(), as the event handler.

        Args:
            observer (List(View)): A list of the observers to be added to
            listen to the model.
        """
        for observer in observers:
            if isinstance(observer, View):
                self.__observers.append(observer)

    def broadcast(self, state:int) -> None:
        """Dispetch the update to all subscribed observers.
        Args:
            state (int): Current state of the model.
        """
        for observer in self.__observers:
            observer.update(state)


class Controller(ABC):
    """Controller for the MVC framework.
    """

    def __init__(self, model: Model) -> None:
        self.__m = model

    @property
    def m(self) -> Model:
        """Model associated with the Controller.
        """
        return self.__m

    @m.setter
    def m(self, m: Model) -> None:
        """Model associated with the Controller.
        """
        self.__m = m


class View(ABC):
    """View for the MVC framework.
    """

    def __init__(self, model: Model,
                 controller: Controller, states: List[int]) -> None:
        """Init method for View.
        params:
            model (Model) : Model of the view.
            controller (Controller): Controller of the view.
            state (str): This is the state with which the view associates. The
                view should be rendered ONLY IF the model's current state is
                set to the state to which the view belongs.
        """
        self.__m = model
        self.__c = controller
        self.__s = states

    def update(self, state:int) -> None:
        """All views are observers of the model. This is the method that the
        model calls when it brocasts.

        params:
            state (int): Current state of the model.
        """
        if any(state == s for s in self.__s):
            self.render()

    @abstractmethod
    def render(self) -> None:
        """All views are observers of the model. This is the method that will
        be executed automatically by self.update() if the model state matches
        the view's associated state.
        """
        pass

    @property
    def m(self) -> Model:
        """Model associated with the View.
        """
        return self.__m

    @m.setter
    def m(self, m: Model) -> None:
        """Model associated with the View.
        """
        self.__m = m

    @property
    def c(self) -> Controller:
        """Controller associated with the View.
        """
        return self.__c

    @c.setter
    def c(self, c: Controller) -> None:
        """Controller associated with the View.
        """
        self.__c = c
