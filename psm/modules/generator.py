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
        computers = self.psm_computer.get_computers_ip_fqdns()
        # filter by scopes
        r = self.psm_scope.filter_computer_dict(computers)
        # filter scopes
        for ip, v in r.items():
            print(f"{ip} {", ".join(v)}")