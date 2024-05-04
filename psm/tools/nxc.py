import os
from psm.logger import psm_logger



class PSMTool():
    name = 'nxc'
    config_name = 'nxc'
    user_isolation_paths = [".nxc"]
    user_config_path = '.nxc'

    def get_locations(self):
        a = []
        for p in self.user_isolation_paths:
            a.append(os.path.join(os.path.expanduser("~/"), p))
        return a