import os
from psm.logger import psm_logger



class PSMTool():
    name = 'nxc'
    #isolation_paths = [".nxc"]
    isolation_paths = [".nxc-psm"]
    user_config_path = '.nxc'

    def get_isolation_paths(self):
        return self.isolation_paths