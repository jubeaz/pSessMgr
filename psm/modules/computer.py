import os
from ast import literal_eval
from libnmap.parser import NmapParser
from fqdn import FQDN

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

    def search_dict(self, field_name=None, pattern=None):
        return self.psm_model.search_dict(field_name=field_name, pattern=pattern)

    def get(self, ip):
        self.psm_model.ip = ip
        self.psm_model.get()
        return self.psm_model

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

    def set_fact(self, fact_key, fact_value):
        self.psm_model.get()
        self.psm_model.set_fact(fact_key, fact_value)
        self.psm_model.update()

    def unset_fact(self, fact_key):
        self.psm_model.get()
        self.psm_model.unset_fact(fact_key)
        self.psm_model.update()

    def get_dict(self):
        return self.psm_model.get_dict()

    def get_ip_fqdns(self):
        result = {}
        tmp = self.psm_model.get_ip_fqdns()
        for t in tmp:
            if t["ip"] not in result:
                fqdns = [] if t["fqdns"] is None else literal_eval(t["fqdns"])
            result[t["ip"]] = fqdns
            if t["computed_fqdn"] is not None:
                result[t["ip"]].append(t["computed_fqdn"])
        return result



    def nmap_import(self, file_path=None, dry_run=False, store_details=False):
        r = NmapParser.parse_fromfile(file_path)
        if store_details:
            self.psm_scan_model.timestamp = r.started
            self.psm_scan_model.file_path = file_path
            self.psm_scan_model.cmdline = r.commandline
            self.psm_scandetail_model.scan_id = r.started
            psm_logger.info("Creating scan")
            self.psm_scan_model.add(dry_run)
        for host in r.hosts:
            if host.is_up():
                self.psm_scandetail_model.ip = host.ipv4
                new = False
                self.psm_model.ip = host.ipv4
                try:
                    self.psm_model.get()
                except Exception:
                    psm_logger.debug(f"New host found {host.ipv4}")
                    new = True
                if new is True:
                    psm_logger.info(f"Adding {host.ipv4}")
                    self.psm_model.add(dry_run)
                    self.psm_model.get()
                for fqdn in host.hostnames:
                    psm_logger.debug(f"Adding {fqdn} to {host.ipv4}")
                    self.psm_model.add_fqdn(fqdn)
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
                        psm_logger.debug(f"Adding service {s_dict} to {host.ipv4}")
                        self.psm_model.add_service(s_dict, dry_run)
                self.psm_model.update(dry_run)

    def import_bloodyad(self, file_path=None, dry_run=False):
        with open(file_path, "r+") as f:
            record = {}
            for line in f:
                if len(line) == 1:
                    if "ip" in record:
                        print(record)
                        print(record["ip"])
                        new = False
                        self.psm_model.ip = record["ip"]
                        try:
                            self.psm_model.get()
                        except Exception:
                            psm_logger.debug(f"New host found {record["ip"]}")
                            new = True
                        if new is True:
                            psm_logger.info(f"Adding {record["ip"]}")
                            self.psm_model.add(dry_run)
                            self.psm_model.get()
                        psm_logger.debug(f"Adding {record["fqdn"]} to {record["ip"]}")
                        try: 
                            self.psm_model.add_fqdn(record["fqdn"])
                        except Exception as e:
                            psm_logger.debug(f"catched {e} but continue ")
                        self.psm_model.update(dry_run)                    
                    record = {}
                    continue
                r = line.split(":")
                if r[0] == "recordName":
                    record["fqdn"] = r[1].replace("\n", "").replace(" ", "")
                if r[0] == "A":
                    record["ip"] = r[1].replace("\n", "").replace(" ", "")

# more complicate since need to find zone record NS,_msdcs,dc03.haas.local.
#  then extract domain and create domain
#  then parse all records
    def import_adidnsdump(self, file_path=None, dry_run=False):
        domain_fqdn = ""
        # first read file to get NS record and grab 
        with open(file_path, "r+") as f:
            for line in f:
                r = line.split(",")
                if r[0] == "NS" and r[1] == "@":
                    fqdn = FQDN(r[2][:-1])
                    domain_fqdn = fqdn.relative.split(".", 1)[1]
        # process A records
        with open(file_path, "r+") as f:
            for line in f:
                r = line.split(",")
                if r[0] != "A":
                    continue
                if r[1] in ["ForestDnsZones", "DomainDnsZones", "@"]:
                    continue
                new = False
                self.psm_model.ip = r[2].replace("\n", "")
                fqdn = f"{r[1]}.{domain_fqdn}"
                try:
                    self.psm_model.get()
                except Exception:
                    psm_logger.debug(f"New host found {r[2]}")
                    new = True
                if new is True:
                    psm_logger.info(f"Adding {r[2]}")
                    self.psm_model.add(dry_run)
                    self.psm_model.get()
                psm_logger.debug(f"Adding {fqdn} to {r[2]}")
                self.psm_model.add_fqdn(fqdn)
                self.psm_model.update(dry_run)
        # process CNAME records
        with open(file_path, "r+") as f:
            for line in f:
                r = line.split(",")
                if r[0] != "CNAME":
                    continue
                fqdn = f"{r[1]}.{domain_fqdn}"
                computer_fqdn = r[2].replace("\n", "")[:-1]
                print(fqdn)
                print(computer_fqdn)
                try:
                    self.psm_model.get(fqdn_pattern=computer_fqdn)
                except Exception:
                    psm_logger.debug(f"Computer not found {computer_fqdn} continue")
                    continue
                psm_logger.debug(f"Adding {fqdn} to {computer_fqdn}")
                self.psm_model.add_fqdn(fqdn)
                self.psm_model.update(dry_run)

    def delete(self):
        self.psm_model.delete_computer()
