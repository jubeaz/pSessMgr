import os
from ast import literal_eval
import ipaddress
from psm.config import current_session
from psm.modules.session import PSMSession
from psm.models.scope import PSMScopeModel
from psm.paths import SESSION_DB_NAME
from psm.logger import psm_logger


class PSMScope:
    psm_model = None

    def __init__(self, scope=None):
        self.psm_session = PSMSession()
        self.psm_session.name = current_session
        self.psm_session.get()
        session_db_path = os.path.join(self.psm_session.full_path, SESSION_DB_NAME)
        self.psm_model = PSMScopeModel(session_db_path)
        self.psm_model.scope = scope

    def _check(self):
        if self.psm_model.scope is None:
            raise RuntimeError("no Scope provided")

    def list(self):
        self.psm_model.list()

    def add(self, excluded):
        self._check()
        self.psm_model.is_excluded = excluded
        self.psm_model.add()

    def delete(self):
        self.psm_model.delete()
