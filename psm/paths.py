import os
import sys
import psm

PSM_PATH = os.path.expanduser("~/.psm")
CONFIG_PATH = os.path.join(PSM_PATH, "psm.conf")
DB_PATH = os.path.join(PSM_PATH, "psm.db")
DATA_PATH = os.path.join(os.path.dirname(psm.__file__), "data")
DEFAULT_CONFIG_PATH = os.path.join(DATA_PATH, "psm.conf")