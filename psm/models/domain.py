import sqlite3 
from os.path import exists
from psm.logger import psm_logger
from tabulate import tabulate
import pandas as dp
#from sqlalchemy import create_engine
from ast import literal_eval

from psm.models.object import PSMObjectModel
#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)


class PSMDomainModel(PSMObjectModel):
    fqdn = None
    netbios = None
    sid = None
    dc_fqdn = None
    is_active = None
    is_target = None

    def __init__(self, session_db_path):
        super().__init__(session_db_path)
        if not self.check_table_exist("domains"):
            psm_logger.info("Creating Computer table")
            self.create_table() 

        # SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';

    def create_table(self):
        try: 
            conn = sqlite3.connect(self.session_db_path)
            c = conn.cursor()
            # try to prevent some weird sqlite I/O errors
            c.execute("PRAGMA journal_mode = OFF")
            c.execute("PRAGMA foreign_keys = 1")
            c.execute(
                """CREATE TABLE if not exists "domains" (
                "fqdn" text PRIMARY KEY,
                "netbios" text,
                "sid" text,
                "dc_fqdn" text, 
                "is_active" boolean,
                "is_target" boolean
                )"""
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def create_constraint(self):
        sql = """PRAGMA foreign_keys=off;
                BEGIN TRANSACTION;
                ALTER TABLE domains RENAME TO domains_old;
                CREATE TABLE if not exists "domains" (
                    "fqdn" text PRIMARY KEY,
                    "netbios" text,
                    "sid" text,
                    "dc_fqdn" text, 
                    "is_active" boolean,
                    "is_target" boolean
                    FOREIGN KEY (dc_fqdn) REFERENCES Computers(fqdn)
                );
                INSERT INTO domains SELECT * FROM domains_old;
                COMMIT;
                PRAGMA foreign_keys=on;"""

    def _check(self):
        if not self.fqdn:
            raise RuntimeError("Domain fqdn not provided")

    def list(self):
        self.list_table("domains")

    def purge(self):
        self.purge_table("domains")

    def get_domains_dict(self):
        return self.get_objects_dict("domains")

    def get(self):
        sql = ''' SELECT netbios, sid, dc_fqdn, is_active, is_target FROM domains 
                  WHERE fqdn = ? '''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.fqdn])
            record = cur.fetchone()
            if record is None:
                psm_logger.error("Domain not found in db")
                raise RecursionError("Domain not found in db")
            self.netbios = record[0]
            self.sid = record[1]
            self.is_active = record[2]
            self.is_target = record[3]
        except sqlite3.Error as e:
            psm_logger.debug(e)
            raise
        finally:
            if conn:
                conn.close()

    def add(self):
        sql = ''' INSERT INTO domains(fqdn, netbios, sid, dc_fqdn, is_active, is_target)
                  VALUES(?, ?, ?, NULL, 0, 0) '''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.fqdn, self.netbios, self.sid])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def update(self):
        sql = ''' UPDATE domains
                    SET netbios = ?, sid = ?, dc_fqdn = ?
                  WHERE fqdn = ?'''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.netbios, self.sid, self.dc_fqdn, self.fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def activate(self):
        sql_d = ''' UPDATE domains
                    SET is_active = 0'''
        sql_a = ''' UPDATE domains
                    SET is_active = 1
                  WHERE fqdn = ?'''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql_d)
            conn.commit()
            cur.execute(sql_a, [self.fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def target(self):
        sql_d = ''' UPDATE domains
                    SET is_target = 0'''
        sql_a = ''' UPDATE domains
                    SET is_target = 1
                  WHERE fqdn = ?'''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql_d)
            conn.commit()
            cur.execute(sql_a, [self.fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def delete(self):
        sql = ''' DELETE FROM domains
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

    def unset_dc(self):
        sql = ''' UPDATE domains
                    SET dc_fqdn = NULL
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
