import os
from psm.logger import psm_logger



class PSMTool():
    name = 'arsenal'
    config_name = 'arsenal'
    isolation_paths = [".arsenal.json"]
    user_config_path = '.arsenal.json'

    def get_isolation_paths(self):
        return self.isolation_paths