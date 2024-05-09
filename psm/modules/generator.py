import os
from psm.config import current_session
from psm.modules.session import PSMSession
from psm.modules.domain import PSMDomain
from psm.modules.computer import PSMComputer
from psm.modules.scope import PSMScope
from psm.paths import SESSION_DB_NAME
from psm.logger import psm_logger



class PSMGenerator:
    psm_computer = None
    psm_domain = None
    psm_scope = None

    def __init__(self):
        self.psm_computer = PSMComputer()
        self.psm_domain = PSMDomain()
        self.psm_scope = PSMScope()



    def export_etc_hosts(self):
        # get hosts
        c_i = self.psm_computer.get_computers_dict()
        c_f = c_i.copy()
        c_ips = c_i.keys()
        for c_ip in c_ips:
            if not c_i[c_ip]["fqdns"]:
                psm_logger.debug(f"removing {c_ip} because no FQDN")
                c_f.pop(c_ip)
        # remove computers without fqdn
        # filter by scopes
        r = self.psm_scope.filter_computer_dict(c_f)
        # filter scopes
        for ip, v in r.items():
            print(f"{ip} {", ".join(v["fqdns"])}")