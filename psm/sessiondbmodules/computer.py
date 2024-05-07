import sqlite3 
from os.path import exists
from psm.logger import psm_logger
from tabulate import tabulate
import pandas as dp
from sqlalchemy import create_engine
from ast import literal_eval

from psm.psmsessiondb import PSMSessionDB

#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)


class PSMSessionComputerDB:
    session_db_path = None
    psm_session_db = None

    def __init__(self, session_db_path):
        self.session_db_path = session_db_path
        self.psm_session_db = PSMSessionDB(session_db_path)
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
                "fqdn" text PRIMARY KEY,
                "name" text,
                "domain_fqdn" text,
                "ip" text,
                "roles" text,
                FOREIGN KEY(domain_fqdn) REFERENCES domains(fqdn)
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


    def add_computer(self, fqdn, name, domain_fqdn, ip, roles):
        sql = ''' INSERT INTO computers(fqdn, name, domain_fqdn, ip, roles)
                  VALUES(?, ?, ?, ?, NULL) '''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [fqdn, name, domain_fqdn, ip])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def update_computer(self, fqdn, ip, roles):
        sql = ''' UPDATE computers
                    SET ip = ?, roles = ? 
                  WHERE fqdn = ?'''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [ip, repr(roles), fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def delete_computer(self, fqdn):
        sql = ''' DELETE FROM computers
                  WHERE fqdn = ?'''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def get_computer(self, fqdn):
        sql = ''' SELECT fqdn, name, domain_fqdn, ip, roles FROM computers 
                  WHERE fqdn = ? '''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [fqdn])
            record = cur.fetchone()
            fqdn = record[0]
            name = record[1]
            domain_fqdn = record[2]
            ip = record[3]
            roles = []
            if record[4] is not None:
                roles = literal_eval(record[4])
        except sqlite3.Error:
            fqdn = None
            name = None
            domain_fqdn = None
            ip = None
            roles = None
            psm_logger.debug(f"{name} domain not found in db")
        finally:
            if conn:
                conn.close()
        return fqdn, name, domain_fqdn, ip, roles

    def list_computer(self):
        self.psm_session_db.list_table("computers")