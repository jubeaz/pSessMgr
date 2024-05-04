import os
from psm.logger import psm_logger



class PSMTool():
    name = 'nxc'
    config_name = 'nxc'
    file_isolation_path = []
    folder_isolation_paths = [".nxc"]
    user_config_path = '.nxc'


    def get_folder_locations(self):
        return self.folder_isolation_paths

    def get_file_locations(self):
        return self.file_isolation_path
