import os
from os.path import dirname, abspath, expanduser, join

# Base paths
DATAPATH = join(dirname(dirname(abspath(__file__))), 'data')
BASEPATH = dirname(dirname(dirname(abspath(__file__))))
HOMEPATH = expanduser("~")


PROJECT_DIRS = [
    "admin",
    "deliverables",
    "evidence/findings",
    "evidence/scans",
    "evidence/scans/vuln",
    "evidence/scans/service",
    "evidence/scans/web",
    "evidence/scans/ad",
    "evidence/osint",
    "evidence/wireless",
    "evidence/logging",
    "evidence/misc",
    "notes",
    "notes/_template",
    "retest",
    "utils/windows",
    "utils/linux"
]

PROJECT_lINKS = [
    ["/opt/windows/windows_weaponize", "utils/windows/windows_weaponize"],
    ["/opt/windows/SharpCollection/NetFramework_4.7_x64", "utils/windows/NetFramework_4.7_x64"]
]

#MODULES =[
#    {
#        name: "SQLMAP",
#        type: 'dir',
#        path: 
#    }
#]