import os
from psm.logger import psm_logger



class PSMTool():
    name = 'arsenal'
    config_name = 'arsenal'
    file_isolation_path = [".arsenal.json"]
    folder_isolation_paths = []
    user_config_path = '.arsenal.json'

    def get_folder_locations(self):
        return self.folder_isolation_paths

    def get_file_locations(self):
        return self.file_isolation_path
