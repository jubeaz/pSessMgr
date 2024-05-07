import os
from psm.config import current_session
from psm.modules.session import PSMSession
from psm.sessiondbmodules.domain import PSMSessionDomainDB
from psm.paths import SESSION_DB_NAME
from psm.logger import psm_logger

class PSMDomain:
    fqdn = ""
    netbios = ""
    sid = ""
    is_active = None
    is_target = None

    def __init__(self, fqdn=None):
        self.fqdn = fqdn
        self._load_session()

    def _load_session(self):
        self.psm_session = PSMSession()
        self.psm_session.name = current_session
        self.psm_session.get()
        session_db_path = os.path.join(self.psm_session.full_path, SESSION_DB_NAME)
        self.psm_session_db = PSMSessionDomainDB(session_db_path)


    def get(self):
        self.fqdn, self.netbios, self.sid, self.is_active, self.is_target = self.psm_session_db.get_domain(self.fqdn)
        if self.fqdn is None:
            psm.logger.error("Domain not found in db")
            raise RecursionError("Domain not found in db")

    def _check(self):
        if not self.fqdn:
            raise RuntimeError("no fqdn provided")

    def add(self, netbios=None, sid=None):
        self._check()
        self.netbios = netbios 
        self.sid = sid 
        self.psm_session_db.add_domain(self.fqdn, self.netbios, self.sid)

    def update(self, netbios=None, sid=None):
        self._check()
        self.get()
        self.netbios = netbios if netbios is not None else self.netbios
        self.sid = sid if sid is not None else self.sid
        self.psm_session_db.update_domain(self.fqdn, self.netbios, self.sid)

    def activate(self):
        self._check()
        self.get()
        self.psm_session_db.activate_domain(self.fqdn)

    def target(self):
        self._check()
        self.get()
        self.psm_session_db.target_domain(self.fqdn)


    def delete(self):
        self._check()
        self.psm_session_db.delete_domain(self.fqdn)

    def list(self):
        self.psm_session_db.list_domain()
