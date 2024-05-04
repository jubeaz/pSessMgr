import os
from psm.logger import psm_logger



class PSMTool():
    name = 'sqlmap'
    config_name = 'sqlmap'
    folder_isolation_paths = [".local/share/sqlmap"]
    file_isolation_path = []
    user_data_path = '.local/share/sqlmap'
    user_config_path = None

    def get_folder_locations(self):
        return self.folder_isolation_paths

    def get_file_locations(self):
        return self.file_isolation_path
