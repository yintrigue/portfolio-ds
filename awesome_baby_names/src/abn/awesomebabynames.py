"""Starting point to initiate AwesomeBabyNames. Note that AwesomeBabyNames
follows the MVC design pattern, so the class merely initiates and connetcs
all the models, controllers, and views.
"""

from abn.models import BabyManager
from abn.controllers import BabyHandler
from abn.menus import MainMenu
from abn.analyzers import TrendAnalyzer
from abn.analyzers import GeoAnalyzer


class AwesomeBabyNames:
    """Class to initiate the Awesome Baby Names program. Note that the program
    is architected using the MVC design pattern.
    """

    def __init__(self) -> None:
        pass

    def main(self) -> None:
        """Initiate and connetcs all the models, controllers, and views.
        """
        # model
        m = BabyManager()
        # controller
        c = BabyHandler(m)
        # views
        v_main_menu = MainMenu(m, c)
        v_trend = TrendAnalyzer(m, c)
        v_geo = GeoAnalyzer(m, c)

        # add views to model as observers
        # notes on the mvc design pattern:
        #     - model will broadcast its state changes to all views
        #     - views will render themselves accordingly depending on the state
        m.add_observers([v_main_menu, v_trend, v_geo])
        m.activate()
