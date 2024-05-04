import os
from psm.logger import psm_logger



class PSMTool():
    name = 'sqlmap'
    config_name = 'sqlmap'
    user_isolation_paths = [".local.share.sqlmap"]
    user_data_path = '.local.share.sqlmap'
    user_config_path = None

    def get_locations(self):
        a = []
        for p in self.user_isolation_paths:
            a.append(os.path.join(os.path.expanduser("~/"), p))
        return a
