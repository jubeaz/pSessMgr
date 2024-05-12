from psm.tools.arsenal import PSMTool
from psm.config import arsenal_defaults_var_values, arsenal_cheat_search_path
import os
import sys
from psm.models.object import PSMObjectModel
from psm.models.computer import PSMComputerModel

def my_tests():
    o = PSMComputerModel("/tmp/titi/.psm_session.db")
    r= o.search_dict("fqdns", "local")
    print(r)