"""The menu module contains all the menu views for AwesomeBabyNames.
"""

from abn.utils.mvc import Model, View
from abn.controllers import BabyHandler
from abn import configs as cf, constants as ct
from typing import Tuple

class MainMenu(View):
    """View class to render the main menu.
    """

    def __init__(self, m: Model, c: BabyHandler) -> None:
        super().__init__(m, c, [ct.STATE.APP_INIT, ct.STATE.MAIN_MENU])

    def render(self) -> None:
        """Render the main menu according to the model's state. Specifically,
        MainMenu handles two states: STATE.MAIN_MENU, STATE.MAIN_MENU
        """
        if super().m.state == ct.STATE.APP_INIT:
            # get user input to determine if db should be loaded
            super().c.on_db_load_request(self.__update_db())
        elif super().m.state == ct.STATE.MAIN_MENU:
            if not super().m.test_db():
                print("Baby names databse not found.")
                print("Please choose to load the database at least once next time you start the program!")
                self.__quit()
            print("")

            # only render the welcome message if user is first visiting the main menu
            if super().m.is_init:
                print("- Awesome Baby Name", cf.APP_VERSION, "-")
                print("Welcome! An awesome baby starts with an awesome name!")
                print("What would you like to do today?")
            else:
                print("Welcome back! What else would you like to do today?")

            self.__render_options()
            self.__get_user_input()

    def __update_db(self) -> None:
        """Get user input to determine if db needs to be updated.
        """
        while True:
            option = input("Refresh or create the baby names datababse (121 MB)? [Y/N] ").strip().lower()
            if len(option) > 0 and option in "yn":
                return option == "y"
            else:
                print("Please enter 'Y' or 'N'...")

    def __render_options(self) -> None:
        """Print all options on the main menu.
        """
        print("[1] Analyze the popularity trend")
        print("[2] Analyze the geographic distribution")
        print("[3] Explore top names by state(s)")
        print("[4] Get name ideas")
        print("[f] View or manage my favorites")
        print("[q] Quit the program")
        print("")

    def __get_user_input(self) -> None:
        option = ""
        counter = 0
        while True:
            option = input(">> ").strip().lower()
            if len(option) > 0 and option in "1234fq":
                # valid input, enter the view mode
                self.__enter_mode(option)
                break
            else:
                # invalid input, print error message
                prefix = ""
                if counter <= 1:
                    print("Please enter a valid option!")
                else:
                    print("Please call customer support if you need help!")
                counter += 1

    def __enter_mode(self, mode: str) -> None:
        """Going from the main menu to sub view modes.

        Args:
            mode (str): View mode to enter.
        """
        switch = {
            "1": [super().c.on_mode_entered, ct.STATE.POPULARITY],
            "2": [super().c.on_mode_entered, ct.STATE.GEO],
            "3": [self.__render_not_ready, None],
            "4": [self.__render_not_ready, None],
            "f": [self.__render_not_ready, None],
            "q": [self.__quit, None]}

        func = switch[mode][0]
        arg = switch[mode][1]
        if arg:
            func(arg)
        else:
            func()

    def __render_not_ready(self) -> None:
        """Render the message to inform user that the content selected is not
        yet ready for the current version.
        """
        print("Sorry, this is not yet ready in {:s}...".format(cf.APP_VERSION))
        self.__get_user_input()

    def __quit(self) -> None:
        """Quit the program. This allows the user to return to the command line.
        """
        print("Thank you for using Awesome Baby Name!")
        super().c.on_quit()
