"""The controller module contains all the controllers for AwesomeBabyNames.
"""

from abn.utils.mvc import Controller
from abn.models import BabyManager
from abn.events import BabyInput
from abn import constants as ct
import sys


class BabyHandler(Controller):
    """BabyHandler handles all the events dispatched from
    AwesomeBabyNames' view classes.
    """

    def __init__(self, m: BabyManager) -> None:
        super().__init__(m)

    def on_db_load_request(self, load:bool) -> None:
        """Event handler for handling user request to create or refreash the db.

        Args:
            load (bool): Set true to load. False to to skip the loading.
        """
        if load:
            super().m.load_db()
        else:
            super().m.skip_load_db()
            super().m.set_state(ct.STATE.MAIN_MENU)

    def on_quit(self) -> None:
        """Event handler for handling user's choice to quit the program.
        """
        sys.exit(0)

    def on_mode_entered(self, mode: int) -> None:
        """Event handler for handling user's choice of analysis mode.

        Args:
            mode (int): View mode to enter.
        """
        super().m.set_state(mode)

    def on_trend_input(self, input_: BabyInput) -> None:
        """Event handler for handling user inputs in trend analysis.

        Args:
            input_ (BabyInput): User inputs for loading the data that are
            required for the trend analysis.
        """
        super().m.input = input_
        super().m.load_trend(input_.name, input_.states)

    def on_geo_input(self, input_: BabyInput) -> None:
        """Event handler for handling user inputs in geo analysis.

        Args:
            input_ (BabyInput): User inputs for loading the data that are
            required for the geo analysis.
        """
        super().m.input = input_
        super().m.load_geo(input_.name, input_.years)

    def on_analysis_complete(self) -> None:
        """Event handler for handling when user finishes an analysis.
        """
        super().m.set_state(ct.STATE.MAIN_MENU)
