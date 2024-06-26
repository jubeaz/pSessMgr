import sqlite3 
from ast import literal_eval
from fqdn import FQDN
import ipaddress

from psm.logger import psm_logger
from psm.models.object import PSMObjectModel


class PSMComputerModel(PSMObjectModel):
# psm_session_db
    ip = None
    fqdns = []
    short_name = None
    domain_fqdns = []
    roles = []
    services = []
    facts = {}

    def __init__(self, session_db_path):
        super().__init__(session_db_path)
        if not self.check_table_exist("computers"):
            psm_logger.info("Creating Computer table")
            self.create_table()


    def create_table(self):
        try: 
            conn = sqlite3.connect(self.session_db_path)
            c = conn.cursor()
            # try to prevent some weird sqlite I/O errors
            c.execute("PRAGMA journal_mode = OFF")
            c.execute("PRAGMA foreign_keys = 1")
            c.execute(
                """CREATE TABLE if not exists "computers" (
                "ip" text PRIMARY KEY,
                "fqdns" text,
                "short_name" text,
                "domain_fqdns" text,
                "roles" text,
                "services" text,
                facts text
                )"""
            )
            # commit the changes and close everything off
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def add_fqdn(self, fqdn, dry_run=False):
        if dry_run is True:
            psm_logger.info("Adding FQDN dry runned")
            return
        if fqdn is None:
            raise RuntimeError("No FQDN")
        f = FQDN(fqdn)
        if not f.is_valid:
            raise RuntimeError("Not a valid FQDN")
        if f.relative not in self.fqdns:
            self.fqdns.append(f.relative)
            name, domain_fqdn = fqdn.split(".", 1)[:2]
            if domain_fqdn not in self.domain_fqdns:
                self.domain_fqdns.append(domain_fqdn)

    def _recompute_domain_fqdn(self):
        tmp = []
        for f in self.fqdns:
            name, domain_fqdn = f.split(".", 1)[:2]
            if domain_fqdn not in tmp:
                tmp.append(domain_fqdn)
        self.domain_fqdns = tmp

    def remove_fqdn(self, fqdn):
        if fqdn is None:
            raise RuntimeError("No FQDN")
        f = FQDN(fqdn)
        if not f.is_valid:
            raise RuntimeError("Not a valid FQDN")
        if f.relative in self.fqdns:
            self.fqdns.remove(f.relative)
            self._recompute_domain_fqdn()    

    def add_role(self, role):
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)

    def add_service(self, service, dry_run=False):
        if dry_run is True:
            psm_logger.info("Adding Service dry runned")
            return 
        if service not in self.services:
            self.services.append(service)

    def remove_service(self, service):
        if service in self.services:
            self.services.remove(service)

    def set_fact(self, fact_key, fact_v, dry_run=False):
        if dry_run is True:
            psm_logger.info("Adding fact dry runned")
            return 
        self.facts[fact_key] = fact_v

    def unset_fact(self, fact_key):
        if fact_key in self.facts:
            self.services.pop(fact_key)

    def _check(self):
        if self.ip is None:
            raise RuntimeError("Computer IP not provided")
        else: 
            try: 
                ipaddress.IPv4Address(self.ip)
            except ipaddress.AddressValueError:
                psm_logger.error(f"{self.ip} is not an IPv4 address")
                raise RuntimeError("IP not compatible") from None

    def get_item_from_record(self, r):
        v = {}
        v["short_name"] = r["short_name"]
        v["fqdns"] = r["fqdns"]
        v["roles"] = r["roles"]
        v["services"] = r["services"]
        v["facts"] = r["facts"]
        if r["fqdns"] is not None:
            v["fqdns"] = literal_eval(r["fqdns"])
        if r["roles"] is not None:
            v["roles"] = literal_eval(r["roles"])
        if r["services"] is not None:
            v["services"] = literal_eval(r["services"])
        if r["facts"] is not None:
            v["facts"] = literal_eval(r["facts"])
        return v        

    def get_dict(self):
        result = {}
        tmp =  self.get_objects_dict("computers")
        for t in tmp:
            v = self.get_item_from_record(t)
            result[t["ip"]] = v
        return result


    def search_dict(self, field_name=None, pattern=None):
        result = {}
        tmp =  self.search_object_dict("computers", field_name=field_name, pattern=field_name)
        for t in tmp:
            v = self.get_item_from_record(t)
            result[t["ip"]] = v
        return result

    def get_ip_fqdns(self):
        sql = "SELECT ip, fqdns, NULL as computed_fqdn from computers where fqdns != '[]'"
        if self.check_table_exist("domains"):
            sql = "select ip, fqdns, fqdn as computed_fqdn from computers as c left join domains as d on d.dc_ip == c.ip where c.fqdns != '[]'"
        try: 
            conn = sqlite3.connect(self.session_db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql)
            records = cur.fetchall()
        except sqlite3.Error as e:
            psm_logger.debug(e)
            raise
        finally:
            if conn:
                conn.close()
        return records


    def list(self):
        self.list_table("computers")

    def purge(self):
        self.purge_table("computers")

    def _reset(self):
        self.fqdns = []
        self.short_name = None
        self.domain_fqdns = []
        self.roles = []
        self.services = []
        self.facts = {}

    def get(self, fqdn_pattern=None):
        if fqdn_pattern:
            sql = """SELECT fqdns, short_name, domain_fqdns, roles, services, facts, ip
                        FROM computers 
                        WHERE fqdns like ? """
        else:
            sql = """SELECT fqdns, short_name, domain_fqdns, roles, services, facts
                        FROM computers 
                        WHERE ip = ? """   
            self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            if fqdn_pattern:
                cur.execute(sql, [f"%{fqdn_pattern}%"])
            else:
                cur.execute(sql, [self.ip])
            record = cur.fetchone()
            if record is None:
                psm_logger.error("Computer not found in db")
                raise RuntimeError("Computer not found in db")
            self._reset()
            self.short_name = record[1]
            if record[0] is not None:
                self.fqdns = literal_eval(record[0])
            if record[2] is not None:
                self.domain_fqdns = literal_eval(record[2])
            if record[3] is not None:
                self.roles = literal_eval(record[3])
            if record[4] is not None:
                self.services = literal_eval(record[4])
            if record[5] is not None:
                self.facts = literal_eval(record[5])
            if fqdn_pattern:
               self.ip = record[6]
        except sqlite3.Error as e:
            psm_logger.debug(e)
            raise
        finally:
            if conn:
                conn.close()

    def add(self, dry_run=False):
        sql = """ INSERT INTO computers(ip, fqdns, short_name, domain_fqdns, roles, services, facts)
                  VALUES(?, NULL, ?, NULL, NULL, NULL, NULL)"""
        if dry_run is True:
            psm_logger.info("Creating computer dry runned")
            return
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.ip, self.short_name])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def update(self, dry_run=False):
        sql = """ UPDATE computers
                    SET short_name = ?, fqdns = ?, roles = ?, domain_fqdns = ?, services = ?, facts = ?
                  WHERE ip = ?"""
        if dry_run is True:
            psm_logger.info("Updating computer dry runned")
            return
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.short_name, repr(self.fqdns), repr(self.roles), repr(self.domain_fqdns), repr(self.services), repr(self.facts),self.ip])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def delete(self):
        sql = """ DELETE FROM computers
                  WHERE fqdn = ?"""
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()
