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
from psm.enums import FilterType

#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)


class PSMScopeModel(PSMObjectModel):
# psm_session_db
    scope = None
    _allow = True

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
                "allow" boolean
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

    def set_filter_type(self, filter_type):
        self._allow = (filter_type.value == FilterType.allow.value) 

    def get_filter_type(self):
        if self._allow is True:
            return FilterType.allow
        return FilterType.block

    def get_default_scoping_action(self):
        scoping_action = self.get_defined_scoping_action()
        if scoping_action is None or scoping_action.value == FilterType.block.value:
            return  FilterType.allow
        return FilterType.block

    def get_defined_scoping_action(self):
        sql = "SELECT allow FROM scopes"
        action = None
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql)
            record = cur.fetchone()
            if record is None:
                action = None
            elif record[0]:
                action = FilterType.allow
            else: 
                action = FilterType.block
        except sqlite3.Error as e:
            psm_logger.debug(e)
            raise
        finally:
            if conn:
                conn.close()            
        return action

    def _check_inclusion_and_types(self):
        existing_scope = self.get_scopes_dict()
        for e in existing_scope:
            if ipaddress.IPv4Network(self.scope).overlaps(ipaddress.IPv4Network(e["scope"])):
                psm_logger.debug(f"{self.scope} overlaps with {e["scope"]}")
                raise RuntimeError("Overlaping scopes")
        if self.get_defined_scoping_action() is not None:
            if self.get_filter_type().value != self.get_defined_scoping_action().value:
                psm_logger.debug(f"{self.scope} allow {self._allow} whereas {e["scope"]} allow {e["allow"]}")
                raise RuntimeError("Scope types mixing")


    def _check_datatype(self):
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

    def _check(self):
        self._check_datatype()
        self._check_inclusion_and_types()

    def list(self):
        self.list_table("scopes")

    def purge(self):
        self.purge_table("scopes")

    def get_dict(self):
        return self.get_objects_dict("scopes")

    def add(self):
        sql = ''' INSERT INTO scopes(scope, allow)
                  VALUES(?, ?)'''
        self._check()
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [self.scope, self._allow])
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

