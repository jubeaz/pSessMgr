import os
from psm.config import current_session
from psm.modules.session import PSMSession
from psm.sessiondbmodules.computer import PSMSessionComputerDB
from psm.paths import SESSION_DB_NAME
from psm.logger import psm_logger
from ast import literal_eval

class PSMComputer:
    fqdn = ""
    name = None
    domain_fqdn = None
    ip = None
    roles = []

    def __init__(self, fqdn=None):
        self.fqdn = fqdn
        if fqdn is not None:
            self.name, self.domain_fqdn = fqdn.split(".", 1)[:2]
        self.roles = []
        self._load_session()

    def _load_session(self):
        self.psm_session = PSMSession()
        self.psm_session.name = current_session
        self.psm_session.get()
        session_db_path = os.path.join(self.psm_session.full_path, SESSION_DB_NAME)
        self.psm_session_db = PSMSessionComputerDB(session_db_path)

    def get(self):
        self.fqdn, self.name, self.domain_fqdn, self.ip, self.roles = self.psm_session_db.get_computer(self.fqdn)
        if self.fqdn is None:
            psm.logger.error("Computer not found in db")
            raise RecursionError("Computer not found in db")

    def _check(self):
        if not self.fqdn:
            raise RuntimeError("no fqdn provided")

    def add(self, ip):
        self._check()
        self.ip =ip 
        self.psm_session_db.add_computer(self.fqdn, self.name, self.domain_fqdn, self.ip, self.roles)


    def update(self, ip):
        self._check()
        self.get()
        self.ip =ip 
        self.psm_session_db.update_computer(self.fqdn, self.ip, self.roles)

    def add_role(self, role):
        self._check()
        self.get()
        if role not in self.roles:
            self.roles.append(role) 
            self.psm_session_db.update_computer(self.fqdn, self.ip, self.roles)

    def remove_role(self, role):
        self._check()
        self.get()
        if role in self.roles:
            self.roles.remove(role) 
            self.psm_session_db.update_computer(self.fqdn, self.ip, self.roles)


    def delete(self):
        self._check() 
        self.psm_session_db.delete_computer(self.fqdn)


    def list(self):
        self.psm_session_db.list_computer()