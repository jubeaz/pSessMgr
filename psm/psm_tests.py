from psm.tools.arsenal import PSMTool
from psm.config import arsenal_defaults_var_values, arsenal_cheat_search_path
import os
import sys

def my_tests():
    src = "~/etc/hosts-psm"
    dst = "/tmp/titi"
    #print(os.path.join(os.path.expanduser(src)))
    #print(os.path.join(os.path.expanduser(dst)))
    if os.path.isabs(src) is not True and src.startswith('~/') is not True:
        raise RuntimeError("must start with / or ~/")
    if os.path.isabs(src):
        print(os.path.join(os.path.expanduser(dst), src[1:]))
    else: 
        print(os.path.join(dst, src[2:]))