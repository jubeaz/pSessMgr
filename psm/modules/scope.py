import os
from ast import literal_eval
from ipaddress import IPv4Address, IPv4Network
from psm.config import current_session
from psm.modules.session import PSMSession
from psm.models.scope import PSMScopeModel
from psm.paths import SESSION_DB_NAME
from psm.logger import psm_logger
from psm.enums import FilterType


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

    def add(self, filter_type):
        self._check()
        self.psm_model.set_filter_type(filter_type)
        self.psm_model.add()

    def get_scopes_dict(self):
        result = {}
        tmp = self.psm_model.get_scopes_dict()
        for t in tmp:
            v = {}
            v["allow"] = t["allow"]
            result[t["scope"]] = v
        return result

    def is_exclusion(self):
        return self.psm_model.is_exclusion()

    # remove blocked computers
    def allow_filter_computer_dict(self, computers):
        c = computers.copy()
        c_ips = computers.keys()
        scopes = self.get_scopes_dict()
        for c_ip in c_ips:
            for s in scopes.keys():
                if IPv4Address(c_ip) in IPv4Network(s):
                    psm_logger.debug(f"{c_ip} remove since belongs to {s}")
                    c.pop(c_ip)
        return c

    # add allowed computers
    def block_filter_computer_dict(self, computers):
        c = {}
        c_ips = computers.keys()
        scopes = self.get_scopes_dict()
        for c_ip in c_ips:
            for s in scopes.keys():
                if IPv4Address(c_ip) in IPv4Network(s):
                    psm_logger.debug(f"{c_ip} add since belongs to {s}")
                    c[c_ip] = computers[c_ip]
        return c

    def filter_computer_dict(self, computers):
        default_scoping_action = self.psm_model.get_default_scoping_action()
        psm_logger.debug(f"Default scoping action {default_scoping_action}")
        if default_scoping_action.value  == FilterType.allow.value:
            return self.allow_filter_computer_dict(computers)
        return self.block_filter_computer_dict(computers)
        



    def delete(self):
        self.psm_model.delete()

    def purge(self):
        self.psm_model.purge()