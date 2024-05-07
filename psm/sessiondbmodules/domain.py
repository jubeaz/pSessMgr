import sqlite3 
from os.path import exists
from psm.logger import psm_logger
from tabulate import tabulate
import pandas as dp
#from sqlalchemy import create_engine
from ast import literal_eval

from psm.psmsessiondb import PSMSessionDB
#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)


class PSMSessionDomainDB:
    session_db_path = None
    psm_session_db = None

    def __init__(self, session_db_path):
        self.session_db_path = session_db_path
        self.psm_session_db = PSMSessionDB(session_db_path)
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
                "main_dc_fqdn" text, 
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


    def add_domain(self, fqdn, netbios, sid):
        sql = ''' INSERT INTO domains(fqdn, netbios, sid, is_active, is_target)
                  VALUES(?, ?, ?, 0, 0) '''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [fqdn, netbios, sid])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def update_domain(self, fqdn, netbios, sid):
        sql = ''' UPDATE domains
                    SET netbios = ?, sid = ?
                  WHERE fqdn = ?'''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [netbios, sid, fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def activate_domain(self, fqdn):
        sql_d = ''' UPDATE domains
                    SET is_active = 0'''
        sql_a = ''' UPDATE domains
                    SET is_active = 1
                  WHERE fqdn = ?'''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql_d)
            conn.commit()
            cur.execute(sql_a, [fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def target_domain(self, fqdn):
        sql_d = ''' UPDATE domains
                    SET is_target = 0'''
        sql_a = ''' UPDATE domains
                    SET is_target = 1
                  WHERE fqdn = ?'''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql_d)
            conn.commit()
            cur.execute(sql_a, [fqdn])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def delete_domain(self, fqdn):
        sql = ''' DELETE FROM domains
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


    def get_domain(self, fqdn):
        sql = ''' SELECT fqdn, netbios, sid, is_active, is_target FROM domains 
                  WHERE fqdn = ? '''
        if not fqdn:
            raise RuntimeError("no fqdn provided")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [fqdn])
            record = cur.fetchone()
            fqdn = record[0]
            netbios = record[1]
            sid = record[2]
            is_active = record[3]
            is_target = record[4]
        except sqlite3.Error:
            fqdn = None
            netbios = None
            sid = None
            is_active = None
            is_target = None
            psm_logger.debug(f"{name} domain not found in db")
        finally:
            if conn:
                conn.close()
        return fqdn, netbios, sid, is_active, is_target

    def list_domain(self):
        self.psm_session_db.list_table("domains")