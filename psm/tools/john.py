import os
from psm.logger import psm_logger
from psm.tools.super.toolsuper import PSMToolSuper


class PSMTool(PSMToolSuper):
    def __init__(self):
        super().__init__('john', ["~/.john"])