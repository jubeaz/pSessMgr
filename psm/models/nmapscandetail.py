import sqlite3 
from os.path import exists
from tabulate import tabulate
import pandas as dp
from sqlalchemy import create_engine
from ast import literal_eval
from fqdn import FQDN
import ipaddress

from psm.logger import psm_logger
from psm.models.object import PSMObjectModel

#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)


## no control since populated from nmap xml


class PSMNmapScanDetailModel(PSMObjectModel):
    id = None
    scan_id = None
    port = None
    proto = None
    state = None
    service = None
    banner = None

    def __init__(self, session_db_path):
        super().__init__(session_db_path)
        if not self.check_table_exist("nmapscan_defail"):
            psm_logger.info("Creating nmapscan_defail table")
            self.create_table()


    def create_table(self):
        try: 
            conn = sqlite3.connect(self.session_db_path)
            c = conn.cursor()
            # try to prevent some weird sqlite I/O errors
            c.execute("PRAGMA journal_mode = OFF")
            c.execute("PRAGMA foreign_keys = 1")
            c.execute(
                """CREATE TABLE if not exists "nmapscan_defail" (
                "id" integer PRIMARY KEY,
                "scan_id" text,
                "ip" text,
                "port" integer,
                "proto" text,
                "state" text,
                "service" text,
                "banner" text
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

    def list(self):
        self.list_table("nmapscan_defail")

    def purge(self):
        self.purge_table("nmapscan_defail")

#    def get(self):
#        sql = ''' SELECT fqdns, short_name, domain_fqdns, roles FROM computers 
#                  WHERE ip = ? '''
#        self._check()
#        try: 
#            conn = sqlite3.connect(self.session_db_path)
#            cur = conn.cursor()
#            cur.execute(sql, [self.ip])
#            record = cur.fetchone()
#            if record is None:
#                psm_logger.error("Computer not found in db")
#                raise RuntimeError("Computer not found in db")
#            if record[0] is not None:
#                self.fqdns = literal_eval(record[0])
#            self.short_name = record[1]
#            if record[2] is not None:
#                self.domain_fqdns = literal_eval(record[2])
#            if record[3] is not None:
#                self.roles = literal_eval(record[3])
#        except sqlite3.Error as e:
#            psm_logger.debug(e)
#            raise
#        finally:
#            if conn:
#                conn.close()

    def add(self, dry_run=False):
        sql = ''' INSERT INTO nmapscan_defail(scan_id, ip, port, proto, state, service, banner)
                  VALUES(?, ?, ?, ?, ?, ?, ?)'''
        if dry_run is True:
            psm_logger.info("Creating scan_detail dry runned")
            return
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.scan_id, self.ip, self.port, self.proto, self.state, self.service, self.banner])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()
        return cur.lastrowid