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


class PSMScopeModel(PSMObjectModel):
# psm_session_db
    scope = None
    is_excluded = False

    def __init__(self, session_db_path):
        super().__init__(session_db_path)
        if not self.check_table_exist("scopes"):
            psm_logger.info("Creating Scopes table")
            self.create_table()


    def create_table(self):
        try: 
            conn = sqlite3.connect(self.session_db_path)
            c = conn.cursor()
            # try to prevent some weird sqlite I/O errors
            c.execute("PRAGMA journal_mode = OFF")
            c.execute("PRAGMA foreign_keys = 1")
            c.execute(
                """CREATE TABLE if not exists "scopes" (
                "scope" text PRIMARY KEY,
                "is_excluded" boolean
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

    def _check(self):
        if self.scope is None:
            raise RuntimeError("No Scope not provided")
        # either IP or network
        else: 
            try: 
                ipaddress.IPv4Address(self.scope)
                self.scope = f"{self.scope}/32"
                return True
            except ipaddress.AddressValueError:
                psm_logger.debug(f"{self.scope} is not an IPv4 address")
            try:
                ipaddress.IPv4Network(self.scope)
            except Exception:
                psm_logger.error(f"{self.scope} is not an IPv4 network address")
                raise RuntimeError("Network address not compatible")


    def list(self):
        self.list_table("scopes")

    def add(self):
        sql = ''' INSERT INTO scopes(scope, is_excluded)
                  VALUES(?, ?)'''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.scope, self.is_excluded])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def delete(self):
        sql = ''' DELETE FROM scopes
                  WHERE scope = ?'''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.scope])
            conn.commit()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def get_scopes(self):
        sql = ''' SELECT * from scopes'''
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