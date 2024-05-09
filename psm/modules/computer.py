import os
from ast import literal_eval
import ipaddress
from psm.config import current_session
from psm.modules.session import PSMSession
from psm.models.computer import PSMComputerModel
from psm.paths import SESSION_DB_NAME
from psm.logger import psm_logger


class PSMComputer:
    psm_model = None

    def __init__(self, ip=None):
        self.psm_session = PSMSession()
        self.psm_session.name = current_session
        self.psm_session.get()
        session_db_path = os.path.join(self.psm_session.full_path, SESSION_DB_NAME)
        self.psm_model = PSMComputerModel(session_db_path)
        self.psm_model.ip = ip

    def _check(self):
        if self.psm_model.ip is None:
            raise RuntimeError("no ip provided")

    def purge(self):
        self.psm_model.purge()

    def list(self):
        self.psm_model.list()

    def add(self, short_name):
        self._check()
        self.psm_model.short_name = short_name
        self.psm_model.add()

    def update(self, short_name):
        self.psm_model.get()
        self.psm_model.short_name = short_name
        self.psm_model.update()


    def add_fqdn(self, fqdn):
        self.psm_model.get()
        self.psm_model.add_fqdn(fqdn)
        self.psm_model.update()

    def remove_fqdn(self, fqdn):
        self.psm_model.get()
        self.psm_model.remove_fqdn(fqdn)
        self.psm_model.update()

    def add_role(self, role):
        self.psm_model.get()
        self.psm_model.add_role(role)
        self.psm_model.update()

    def remove_role(self, role):
        self.psm_model.get()
        self.psm_model.remove_role(role)
        self.psm_model.update()

    def get_computers_dict(self):
        result = {}
        tmp = self.psm_model.get_computers_dict()
        for t in tmp:
            v = {}
            if t["fqdns"] is None:
                v["fqdns"] = []
            else:     
                v["fqdns"] = literal_eval(t["fqdns"])
            result[t["ip"]] = v
        return result

    def delete(self):
        self.psm_model.delete_computer()
