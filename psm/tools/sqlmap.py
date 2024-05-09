import os
from psm.logger import psm_logger



class PSMTool():
    name = 'sqlmap'
    #isolation_paths = [".local/share/sqlmap"]
    isolation_paths = ["~/.local/share/sqlmap-psm"]
    isolation_paths_dict = {
        "~/.local/share/sqlmap-psm": ".local/share/sqlmap-psm"
        }
    user_data_path = '.local/share/sqlmap'
    user_config_path = None

    def get_isolation_paths_old(self):
        return self.isolation_paths

    def get_isolation_paths(self, dst):
        p = []
        for src in self.isolation_paths:
            if os.path.isabs(src) is not True and src.startswith('~/') is not True:
                raise RuntimeError("must start with / or ~/")
            e = {}
            if os.path.isabs(src):
                e["dst"] = os.path.join(os.path.expanduser(dst), src[1:])
                e["src"] = src
            else: 
                e["dst"] = os.path.join(dst, src[2:])
                e["src"] = os.path.expanduser(src)
            p.append(e)
        psm_logger.debug(p)
        return p
