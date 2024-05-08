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

    def list(self):
        self.psm_model.list_computer()

    def add(self, short_name):
        self._check()
        self.psm_model.short_name = short_name
        self.psm_model.add_computer()

    def update(self, short_name):
        self.psm_model.get()
        self.psm_model.short_name = short_name
        self.psm_model.update_computer()


    def add_fqdn(self, fqdn):
        self.psm_model.get()
        self.psm_model.add_fqdn(fqdn)
        self.psm_model.update_computer()

    def remove_fqdn(self, fqdn):
        self.psm_model.get()
        self.psm_model.remove_fqdn(fqdn)
        self.psm_model.update_computer()

    def add_role(self, role):
        self.psm_model.get()
        self.psm_model.add_role(role)
        self.psm_model.update_computer()

    def remove_role(self, role):
        self.psm_model.get()
        self.psm_model.remove_role(role)
        self.psm_model.update_computer()

    def export_etc_hosts(self):
        res = self.psm_model.get_computers()
        for r in res:
            ip = r["ip"]
            fqdns = literal_eval(r["fqdns"])
            print(f"{ip} {', '.join(fqdns)}")

    def delete(self):
        self.psm_model.delete_computer()
