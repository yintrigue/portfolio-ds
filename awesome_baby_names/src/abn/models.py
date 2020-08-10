"""The model module contains all the models for AwesomeBabyNames.
"""

from abn.utils.mvc import Model
from abn.events import BabyInput
from abn.utils import performance as pf
from abn import constants as ct, configs as cf
from typing import Tuple
import sqlite3
import pandas as pd
import glob
import os


class BabyManager(Model):
    """BabyLoader manges all the business lgoics of AwesomeBabyNames including
    data loading/parsing and state management.
    """

    def __init__(self) -> None:
        super().__init__()
        # constants.STATE
        self.__state = ""
        self.__state_change_counter = 0
        # BabyInput, input received from the users
        self.__input = None
        # pd.DataFrame, data loaded according user inputs
        self.__df = None

    def activate(self) -> None:
        """Activate the model.
        """
        self.set_state(ct.STATE.APP_INIT)

    def load_db(self) -> None:
        """Load or update the baby names databse.
        """
        loader = BabyLoader()
        loader.load_raw_csv()

        # deafult to main menu
        self.set_state(ct.STATE.MAIN_MENU)

    def load_trend(self, name: str, states: Tuple[str]) -> None:
        """Load daata for the trend analysis.

        Args:
            name (str): Name of the baby to be analyzed.
            states (Tuple[str]): States to be included for the analysis.
        """
        self.__df = BabyLoader.get_instance().load_trend(name, states)
        super().broadcast(self.__state)

    def load_geo(self, name: str, years: Tuple[int]) -> None:
        """Load daata for the geo analysis.

        Args:
            name (str): Name of the baby to be analyzed.
            years (Tuple[int]): [0] is the starting year. [1] is the ending year.
        """
        self.__df = BabyLoader.get_instance().load_geo(name, years)
        super().broadcast(self.__state)

    def set_state(self, s: int) -> None:
        """Set the state for the model.

        Args:
            s (int): State of the model. Refer to abn.constants.STATE.
        """
        # clean up data when entering a new state
        self.__df = None
        self.__state_change_counter += 1

        self.__state = s
        super().broadcast(self.__state)

    def test_db(self) -> bool:
        """Test if the baby names database exists.
        Retuns:
            bool: True if database if found. False otherwise.
        """
        return BabyLoader.get_instance().test_db()

    def skip_load_db(self) -> None:
        """Skip loading the db. The baby names DB is assumed to already
        exist if skipped.
        """
        BabyLoader.get_instance().skip_load_raw_csv()

    @property
    def state(self) -> str:
        """State of the model.
        """
        return self.__state

    @property
    def df(self) -> pd.DataFrame:
        """Data loaded for the current state.
        """
        return self.__df

    @property
    def is_init(self) -> str:
        """True if model has been initialized. False otherwise.
        """
        return self.__state_change_counter <= 1

    @property
    def input(self) -> BabyInput:
        """User inputs received for the current state.
        """
        return self.__input

    @input.setter
    def input(self, input_:BabyInput) -> None:
        """User inputs required for the current state.
        """
        self.__input = input_


class BabyLoader:
    """BabyLoader loads the data required data for analysis modes. Note that
    BabyLoader is a singleton. The design is to prvent memory waste by disallowing
    the same external data to be loaded to memory through multiple BabyLoader initiations.
    """

    __instance = None

    @staticmethod
    def get_instance():
        """Return an instance of the singleton BabyLoader.
        """
        if BabyLoader.__instance == None:
            BabyLoader()
        return BabyLoader.__instance

    def __init__(self) -> None:
        if BabyLoader.__instance:
            raise Exception("BabyLoader cannot be initiated directly...")
        else:
            BabyLoader.__instance = self

        self.__is_loaded = False
        self.__db_connection = None # Connection

    def test_db(self) -> bool:
        """Test if the DB exists.

        Returns:
            bool: True if DB is detected. False otherwise.
        """
        return os.path.isfile(cf.SQL_LITE.PATH + cf.SQL_LITE.DB)

    def skip_load_raw_csv(self) -> None:
        """Invoke this method if user chooses to skip loading the raw csv and
        create or refresh the baby names db. The db is simply assumed to exist locally.
        """
        self.__is_loaded = True

    def load_raw_csv(self) -> None:
        """Load the raw csv for the baby names DB.
        """
        # drop the baby_names table to get a fresh set of data
        self.__query_write("DROP TABLE IF EXISTS " + cf.SQL_LITE.TABLE_BABY_NAMES)

        # get the path for csv files
        con = self.__get_db()
        files = []
        for p in cf.BABY_FILES.PATHS:
            files = glob.glob(p + "*." + cf.BABY_FILES.EXTENSION)
            if len(files) > 0:
                break

        # load csv
        for i, file in enumerate(files):
            df = pd.read_csv(file, index_col=None, header=None,
                    names=["state", "gender", "year", "baby_name", "count"])

            size_mb = os.path.getsize(file) / 1000000
            n = len(files)

            # this prints messages to terminal; an ugly 'hack' to get messages out quickly...
            print("[{:0>2d}/{:0>2d}] Loading {:.2f} MB of babies from {:s}..."
                  .format(i+1, n, size_mb, df["state"][0]))
            df.to_sql(cf.SQL_LITE.TABLE_BABY_NAMES, con=con, if_exists='append')
        self.__close_db()

        self.__is_loaded = True

    def load_trend(self, name: str, states: Tuple[str]) -> pd.DataFrame:
        """Load the data required for the trend analysis.

        Args:
            name (str): Name of the baby.
            states (Tuple[str]): States selected for the analysis.
        """
        if not self.__is_loaded:
            return

        # prep sql
        sql_states = ",".join("'{:s}'".format(state.lower()) for state in states)
        sql = "SELECT count, year, gender" + \
               " FROM " + cf.SQL_LITE.TABLE_BABY_NAMES + \
               " WHERE " + \
               " lower(baby_name)='{:s}' AND".format(name.lower()) + \
               " lower(state) IN ({:s})".format(sql_states)

        # load & parse data
        df = None
        if cf.DEBUG_MODE:
            # time the performance in debug mode
            df = pf.time_it(self.__query_read)(sql)
        else:
            df = self.__query_read(sql)
        df = df.groupby(["year", "gender"]).sum().reset_index()

        return df

    def load_geo(self, name: str, years: Tuple[int]) -> pd.DataFrame:
        """Load the data required for the trend analysis.

        Args:
            name (str): Name of the baby.
            years (Tuple[int]): Timespan for the geo analysis. [0] is the
            starting eyar. [1] is the ending year.
        """
        if not self.__is_loaded:
            return

        # prep sql
        sql = "SELECT count, gender, state" + \
               " FROM " + cf.SQL_LITE.TABLE_BABY_NAMES + \
               " WHERE " + \
               " lower(baby_name)='{:s}' AND".format(name.lower()) + \
               " year BETWEEN {:d} AND {:d}".format(years[0], years[1])

        # load & parse data
        df = None
        if cf.DEBUG_MODE:
            # time the performance in debug mode
            df = pf.time_it(self.__query_read)(sql)
        else:
            df = self.__query_read(sql)
        df = df.groupby(["state", "gender"]).sum().reset_index()

        return df

    def __query_read(self, sql:str) -> pd.DataFrame:
        """Private method to read the queries from the baby names DB.
        """
        # load data
        con = self.__get_db()
        df = pd.read_sql(sql, con)
        self.__close_db()

        return df

    def __query_write(self, sql:str) -> None:
        """Private method to write the queries from the baby names DB.
        """
        con = self.__get_db()
        cursor_ = con.cursor()
        cursor_.execute(sql)
        con.commit()
        self.__close_db()

    def __get_db(self) -> sqlite3.Connection:
        """Private method to get baby names DB.

        Returns:
            sqlite3.Connection: Connection to the baby names DB.
        """
        # if self.__db_connection == None:
        self.__db_connection = sqlite3.connect(cf.SQL_LITE.PATH + cf.SQL_LITE.DB)

        return self.__db_connection

    def __close_db(self) -> None:
        """Close the connection to the baby names DB.
        """
        if self.__db_connection != None:
            self.__db_connection.close()
