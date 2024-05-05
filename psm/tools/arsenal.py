import os
from psm.logger import psm_logger



class PSMTool():
    name = 'arsenal'
    #isolation_paths = [".arsenal.json"]
    isolation_paths = [".arsenal.json-psm"]
    user_config_path = '.arsenal.json'

    def get_isolation_paths(self):
        return self.isolation_paths