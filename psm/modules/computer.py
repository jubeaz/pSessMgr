import os
from ast import literal_eval
import ipaddress
from libnmap.parser import NmapParser

from psm.config import current_session
from psm.modules.session import PSMSession
from psm.models.computer import PSMComputerModel
from psm.models.nmapscan import PSMNmapScanModel
from psm.models.nmapscandetail import PSMNmapScanDetailModel
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
        self.psm_scan_model = PSMNmapScanModel(self.psm_model.session_db_path)
        self.psm_scandetail_model = PSMNmapScanDetailModel(self.psm_model.session_db_path)

    def _check(self):
        if self.psm_model.ip is None:
            raise RuntimeError("no ip provided")

    def purge(self):
        self.psm_model.purge()
        self.psm_scan_model.purge()
        self.psm_scandetail_model.purge()

    def list(self):
        self.psm_model.list()
        self.psm_scan_model.list()
        self.psm_scandetail_model.list()

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
        self.psm_model.add_fqdn(fqdn, dry_run)
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


    def nmap_import(self, file_path=None, dry_run=False, store_details=False):
        r = NmapParser.parse_fromfile(file_path)

        print(f'store_details is {store_details}')
        if store_details:
            self.psm_scan_model.timestamp = r.started
            self.psm_scan_model.file_path = file_path
            self.psm_scan_model.cmdline = r.commandline
            self.psm_scandetail_model.scan_id = r.started
            psm_logger.info("Creating scan")
            print(f'store_details is {store_details}')
            self.psm_scan_model.add(dry_run)
        for host in r.hosts:
            if host.is_up():
                self.psm_scandetail_model.ip = host.ipv4
                new = False
                self.psm_model.ip = host.ipv4
                try:
                    self.psm_model.get()
                except:
                    psm_logger.info(f"New host found {host.ipv4}")
                    new = True
                if new is True:
                    psm_logger.info(f"Adding {host.ipv4}")
                    self.psm_model.add(dry_run)
                for fqdn in host.hostnames:
                    psm_logger.debug(f"Adding {fqdn} to {host.ipv4}")
                    self.psm_model.add_fqdn(fqdn)
                    self.psm_model.update(dry_run)
                for s in host.services:
                    if store_details:
                        self.psm_scandetail_model.status = s.state
                        self.psm_scandetail_model.port = s.port
                        self.psm_scandetail_model.proto = s.protocol
                        self.psm_scandetail_model.service = s.service
                        self.psm_scandetail_model.banner = s.banner
                        self.psm_scandetail_model.add(dry_run)
                        s_str = f"[{s.state}] {s.port}/{s.protocol} {s.service} ({s.banner})"
                        psm_logger.info(f"Adding {s_str} to nmapscan_detail")
                    if s.state == "open":
                        s_dict = {}
                        s_dict[f"{s.port}/{s.protocol}"] =  s.service
                        psm_logger.info(f"Adding service {s_dict} to {host.ipv4}")
                        self.psm_model.add_service(s_dict, dry_run)
                        self.psm_model.update(dry_run)


    def delete(self):
        self.psm_model.delete_computer()
