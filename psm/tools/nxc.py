import os
from psm.logger import psm_logger



class PSMTool():
    name = 'nxc'
    config_name = 'nxc'
    isolation_paths = [".nxc"]
    user_config_path = '.nxc'

    def get_isolation_paths(self):
        return self.isolation_paths