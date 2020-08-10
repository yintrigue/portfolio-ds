"""The configs module includes all the config constants used
across AwesomeBabyNames.
"""

from collections import namedtuple

DEBUG_MODE = True

# set True to use Pandas to plot; otherwise, plots will be
# createdusing termplotlib
PANDAS_PLOT = False

APP_VERSION = 'Beta 1.3.7'

MAX_STATES_ALLOWED = 10

TERM_PLOT = namedtuple("TERM_PLOT", ())
TERM_PLOT.W = 100
TERM_PLOT.H = 25
TERM_PLOT.FORCE_ASCII = True

PLOT_TREND = namedtuple("PLOT_TREND", ())
PLOT_TREND.X = "Year"
PLOT_TREND.Y = "No. of Babies Baorn"

BABY_FILES = namedtuple("BABY_FILES", ())
BABY_FILES.PATHS = ["../data/", "./data/"]
BABY_FILES.EXTENSION = "CSV"

SQL_LITE = namedtuple("SQL_LITE", ())
SQL_LITE.PATH = "./"
SQL_LITE.DB = "babies.db"
SQL_LITE.TABLE_BABY_NAMES = "tbl_baby_names"
