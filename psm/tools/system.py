import os
from psm.logger import psm_logger



class PSMTool():
    name = 'system'
    #isolation_paths = ["/etc/hosts"]
    isolation_paths = ["/etc/hosts-psm", "/etc/krb5.conf"]
    user_data_path = ''
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
        psm_logger.info("Remember to perform a 'sudo -E chown --recursive <user>:<group> ~/.psm")
        psm_logger.info(f"Remember to perform a 'sudo -E chown --recursive <user>:<group> {dst}")
        return p
