import os
from psm.config import current_session
from psm.modules.session import PSMSession
from psm.models.domain import PSMDomainModel
from psm.paths import SESSION_DB_NAME
from psm.logger import psm_logger

class PSMDomain:
    psm_model = None


    def __init__(self, fqdn=None):
        self.psm_session = PSMSession()
        self.psm_session.name = current_session
        self.psm_session.get()
        session_db_path = os.path.join(self.psm_session.full_path, SESSION_DB_NAME)
        self.psm_model = PSMDomainModel(session_db_path)
        self.psm_model.fqdn = fqdn

#    def get(self):
#        self.fqdn, self.netbios, self.sid, self.is_active, self.is_target = self.psm_model.get_domain(self.fqdn)
#        if self.fqdn is None:
#            psm.logger.error("Domain not found in db")
#            raise RuntimeError("Domain not found in db")

    def _check(self):
        if self.psm_model.fqdn is None:
            raise RuntimeError("no fqdn provided")

    def list(self):
        self.psm_model.list()

    def purge(self):
        self.psm_model.purge()

    def add(self, netbios=None, sid=None):
        self._check()
        self.psm_model.netbios = netbios 
        self.psm_model.sid = sid 
        self.psm_model.add()

    def update(self, netbios=None, sid=None, dc_fqdn=None):
        self.psm_model.get()
        self.psm_model.netbios = netbios if netbios is not None else self.psm_model.netbios
        self.psm_model.sid = sid if sid is not None else self.psm_model.sid
        self.psm_model.dc_fqdn = dc_fqdn if dc_fqdn is not None else self.psm_model.dc_fqdn
        self.psm_model.update()

    def activate(self):
        self.psm_model.get()
        self.psm_model.activate()

    def target(self):
        self.psm_model.get()
        self.psm_model.target()

    def unset_dc(self):
        self.psm_model.unset_dc()

    def delete(self):
        self.psm_model.delete()
