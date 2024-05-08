import sqlite3 
from os.path import exists
from tabulate import tabulate
import pandas as dp
from sqlalchemy import create_engine
from ast import literal_eval
from fqdn import FQDN

from psm.logger import psm_logger
from psm.models.object import PSMObjectModel

#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)


class PSMComputerModel(PSMObjectModel):
# psm_session_db
    ip = None
    fqdns = []
    short_name = None
    domain_fqdns = []
    roles = []

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
                "roles" text
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



    def add_fqdn(self, fqdn):
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

    def _check(self):
        if not self.ip:
            raise RuntimeError("Computer IP not provided")

    def list_computer(self):
        self.list_table("computers")

    def get(self):
        sql = ''' SELECT fqdns, short_name, domain_fqdns, roles FROM computers 
                  WHERE ip = ? '''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.ip])
            record = cur.fetchone()
            if record is None:
                psm_logger.error("Computer not found in db")
                raise RecursionError("Computer not found in db")
            if record[0] is not None:
                self.fqdns = literal_eval(record[0])
            self.short_name = record[1]
            if record[2] is not None:
                self.domain_fqdns = literal_eval(record[2])
            if record[3] is not None:
                self.roles = literal_eval(record[3])
        except sqlite3.Error as e:
            psm_logger.debug(e)
            raise
        finally:
            if conn:
                conn.close()

    def add_computer(self):
        sql = ''' INSERT INTO computers(ip, fqdns, short_name, domain_fqdns, roles)
                  VALUES(?, NULL, ?, NULL, NULL)'''
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

    def update_computer(self):
        sql = ''' UPDATE computers
                    SET short_name = ?, fqdns = ?, roles = ?, domain_fqdns = ?
                  WHERE ip = ?'''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.short_name, repr(self.fqdns), repr(self.roles), repr(self.domain_fqdns), self.ip])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def delete_computer(self):
        sql = ''' DELETE FROM computers
                  WHERE fqdn = ?'''
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