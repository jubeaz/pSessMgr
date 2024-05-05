import os
from psm.logger import psm_logger



class PSMTool():
    name = 'sqlmap'
    config_name = 'sqlmap'
    #isolation_paths = [".local/share/sqlmap"]
    isolation_paths = [".local/share/sqlmap-psm"]
    user_data_path = '.local/share/sqlmap'
    user_config_path = None

    def get_isolation_paths(self):
        return self.isolation_paths