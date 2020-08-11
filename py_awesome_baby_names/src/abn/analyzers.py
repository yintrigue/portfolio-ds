"""The analyzers module contain all the views responsible for rendering
the analysis modes user enters.
"""

from abn.utils.mvc import Model, View, Controller
from abn.events import BabyInput
from abn import configs as cf, constants as ct
from typing import Tuple, List
import pandas as pd
import termplotlib as tpl
import matplotlib.pyplot as plt


class AnalyzerView(View):
    """Abstract view class that contains common methods used across analyzer
    views. This class is to be inherited, and must not be initatied alone.
    """

    def __init__(self, m: Model, c: Controller, state:List[str]) -> None:
        super().__init__(m, c, state)

    def get_baby_name(self, line_break: bool=False) -> str:
        """ Get baby's name from user.

        Args:
            line_break (bool): Set True to display user input request on a new
                line after the prompt message.

        Returns:
            (str): Name of the baby entered by the user.
        """
        name = ""
        if line_break:
            print("Eneter a baby's name:")
        while True:
            if not line_break:
                name = input("Eneter a baby's name: ").strip()
            else:
                name = input(">> ").strip()

            # validation
            if type(name) is str and all([char.isalpha() for char in name]):
                return name
            else:
                print("A baby's name should only contain alphabets...")

    def get_states(self) -> Tuple[str]:
        """ Get states from user.

        Returns:
            (Tuple[str]): A list of the states entered by the user.
        """

        print("You can enter up to 10 states separated by whitespace (e.g. 'AL AK CA').")
        while True:
            states = tuple(input("Eneter state(s): ").strip().upper().split())

            # validation
            if all([state not in ct.US_STATES for state in states]):
                print("One or more invalid states...")
            elif all([states.count(state) >= 2 for state in states]):
                print("One or more duplicate states...")
            elif len(states) > cf.MAX_STATES_ALLOWED:
                print("Only up to {:0d} states are allowed...".format(cf.MAX_STATES_ALLOWED))
            else:
                return states

    def get_years(self) -> Tuple[int]:
        """ Get states from user.

        Returns:
            (List[int]): Year interval. [0] is the starting year. [1] is
            the end year.
        """
        print("A timespan is two years seperated by whitespace.")
        while True:
            years = input("Eneter a timespan: ").strip().upper().split()
            try:
                years = tuple([int(year) for year in years])
            except:
                print("One or more invalid years...")
                continue

            # validation
            if len(years) != 2:
                print("Please enter exactly two year numbers...")
            elif any([year < 1910 or year > 2018 for year in years]):
                print("Only years between 1910 and 2018 can be analyzed...")
            else:
                return years


class TrendAnalyzer(AnalyzerView):
    """View to render the popularity trend analysis mode.
    """

    def __init__(self, m: Model, c: Controller) -> None:
        super().__init__(m, c, [ct.STATE.POPULARITY])

    def render(self) -> None:
        """All views are observers of the model. This is the method that the
        model calls when it brocasts.
        """
        # get inputs if model does not data; othwersie, render the data
        if super().m.df is None:
            print("")
            print("- Popularity Analysis -")
            print(("Popularity Analysis allows you to analyze the popularity "
                   "trend of your chosen baby's name."))

            # get user input & update controller
            input_ = self.__get_user_input()
            print("Loading babies...")
            super().c.on_trend_input(input_)
        else:
            self.__plot()

    def __get_user_input(self) -> BabyInput:
        """Get user inputs for the popularity trend analysis.

        Returns:
            BabyInput: Inputs from the user required for the trend analysis.
        """
        input_ = BabyInput()
        input_.name = super().get_baby_name()
        input_.states = super().get_states()

        return input_

    def __plot(self) -> None:
        """Create plots by pulling relevent data from the model.
        """

        # prep title
        baby_name = super().m.input.name
        states = list(super().m.input.states)
        state_last = states.pop()
        states_str = ", ".join(states) + " and " + state_last
        title = "'{:s}' in {:s}".format(baby_name, states_str)

        df = super().m.df
        if not df.empty:
            if cf.PANDAS_PLOT:
                # plot using matplotlib
                title = "Baby " + title
                df = df.pivot(index="year", columns="gender", values="count")
                ax = df.plot(kind="line", title=title)
                ax.set_xlabel(cf.PLOT_TREND.X)
                ax.set_ylabel(cf.PLOT_TREND.Y)
                plt.show()
            else:
                # plot using termplotlib
                # plot male babies
                print("")
                p_succes = self.__plot_term(df[df.gender=="M"], "Baby Boy " + title)
                if p_succes:
                    print("\n")
                # render female babies
                self.__plot_term(df[df.gender=="F"], "Baby Girl " + title)
        else:
            print("Sorry, can't find any baby...")

        print("\nReturning to main menu...")
        super().c.on_analysis_complete()

    def __plot_term(self, df:pd.DataFrame, title) -> bool:
        """Generic method to plot using the termplotlib module.

        Args:
            df (pd.DataFrame): Data used to render the plot.
            title (str): Title to be displayed on top of the plot.
        """
        if not df.empty:
            fig = tpl.figure()
            fig.plot(x=df["year"], y=df["count"],
                     title=title, width=cf.TERM_PLOT.W, height=cf.TERM_PLOT.H, ylim=[0, None])
            fig.show()
            return True
        else:
            return False


class GeoAnalyzer(AnalyzerView):
    """View to render the geo analysis mode.
    """

    def __init__(self, m: Model, c: Controller) -> None:
        super().__init__(m, c, [ct.STATE.GEO])

    def render(self) -> None:
        """All views are observers of the model. This is the method that the
        model calls when it brocasts.
        """

        # get inputs if model does not data; othwersie, render the data
        if super().m.df is None:
            print("")
            print("- Geo Distribution Analysis -")
            print(("Geo Distribution Analysis allows you to analyze how popular "
                   "your chosen baby's name is across states."))

            # get user input & update controller
            input_ = self.__get_user_input()
            print("Loading babies...")
            super().c.on_geo_input(input_)
        else:
            self.__plot()

    def __get_user_input(self) -> BabyInput:
        """Get user inputs for the geo distribution analysis.

        Return:
            BabyInput: Inputs from the user required for the geo analysis.
        """

        input_ = BabyInput()
        input_.name = super().get_baby_name()
        input_.years = super().get_years()

        return input_

    def __plot(self) -> None:
        """Create plots by pulling relevent data from the model.
        """

        # prep title
        baby_name = super().m.input.name
        years = super().m.input.years
        title = "'{:s}' From {:d} To {:d}".format(baby_name, years[0], years[1])

        df = super().m.df
        if not df.empty:
            if cf.PANDAS_PLOT:
                print("Plot not available...")
            else:
                # plot using termplotlib
                self.__plot_term(df[df.gender=="M"], "Baby Boy " + title)
                self.__plot_term(df[df.gender=="F"], "Baby Girl " + title)
        else:
            print("Sorry, can't find any baby...")

        print("\nReturning to main menu...")
        super().c.on_analysis_complete()

    def __plot_term(self, df: pd.DataFrame, title) -> bool:
        """Generic method to plot using the termplotlib module.

        Args:
            df (pd.DataFrame): Data used to render the plot.
            title (str): Title to be displayed on top of the plot.

        Returns:
            bool: True if plot is rendered successfully. False otherwise.
        """

        if not df.empty:
            print("")
            print(title)
            fig = tpl.figure()
            fig.barh(
                df["count"].values.tolist(),
                df["state"].values.tolist(),
                force_ascii=cf.TERM_PLOT.FORCE_ASCII,
                max_width=cf.TERM_PLOT.W
            )
            fig.show()

            return True
        else:
            return False
