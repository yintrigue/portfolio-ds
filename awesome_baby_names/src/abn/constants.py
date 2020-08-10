"""The constants module includes all the constants used across AwesomeBabyNames.
"""

from abn import configs as cf
from collections import namedtuple
import glob
import os

# state for the state diagrams
STATE = namedtuple("STATE", ())
STATE.APP_INIT = 0
STATE.MAIN_MENU = 1
STATE.POPULARITY = 2
STATE.GEO = 3

# states allowed depends on the data avaliable
US_STATES = set()
files = []
for p in cf.BABY_FILES.PATHS:
    files = glob.glob(p + "*." + cf.BABY_FILES.EXTENSION)
    if len(files) > 0:
        for file in files:
            base = os.path.basename(file)
            US_STATES.add(os.path.splitext(base)[0])
        break

GENDER = namedtuple("GENDER", ())
GENDER.FEMALE = 0
GENDER.MALE = 1
GENDER.UKNOWN = 2
