from enum import Enum

class FilterType(str, Enum):
    allow = "allow"
    block = "block"


class ComputerRole(str, Enum):
    dc = "dc"
    smb = "smb"
    mssql = "mssql"