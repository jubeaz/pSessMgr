import sqlite3 
from tabulate import tabulate
import pandas as dp
from sqlalchemy import create_engine
from ast import literal_eval
from os.path import exists

from psm.logger import psm_logger
from psm.paths import SESSION_DB_NAME

class PSMObjectModel:
    session_db_path = None
    psm_session = None

    def __init__(self, session_db_path):
        self.session_db_path = session_db_path
        if not exists(session_db_path):
            self.create_db()
            psm_logger.info(f"[*] Session database created {session_db_path}")

    def create_db(self):
        if exists(self.session_db_path):
            psm_logger.error(f"Creation requested but {self.session_db_path} already exist")
            raise RuntimeError("Session DB exist")
        try: 
            conn = sqlite3.connect(self.session_db_path)
            c = conn.cursor()
            # try to prevent some weird sqlite I/O errors
            c.execute("PRAGMA journal_mode = OFF")
            c.execute("PRAGMA foreign_keys = 1")
            # commit the changes and close everything off
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def list_table(self, table_name):
        try: 
            conn = sqlite3.connect(self.session_db_path)
            tb_ss = dp.read_sql(f"SELECT * FROM {table_name}", conn)
            psm_logger.info(tabulate(tb_ss, showindex=False, headers=tb_ss.columns, tablefmt='grid'))
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()

    def purge_table(self, table_name):
        sql = f"DELETE from {table_name}"
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            psm_logger.debug(f"Executing {sql}")
        except sqlite3.Error as e:
            psm_logger.debug(e)
            raise
        finally:
            if conn:
                conn.close()

    def check_table_exist(self, name):
        sql = '''SELECT name 
                FROM sqlite_master 
                WHERE  name = ?'''
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [name])
            record = cur.fetchone()
        except Exception as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()
        return record is not None

    def get_table_fkeys(self, name):
        sql= """PRAGMA foreign_key_list(?)"""
        raise RuntimeError("todo")

    def get_table_fields(self, name):
        sql= """select name from pragma_table_info(?) as tblInfo;"""
        names = []
        try: 
            conn = sqlite3.connect(self.session_db_path)
            cur = conn.cursor()
            cur.execute(sql, [name])
            records = cur.fetchall()
        except Exception as e:
            psm_logger.error(e)
            if conn:
                conn.close()
            raise
        for record in records:
            names.append(record[0])
        conn.close()
        return names

    def search_object_dict(self, table_name, field_name, pattern):
        if field_name not in self.get_table_fields(table_name):
            raise RuntimeError("Invalid field name for search_dict")
        sql = f"SELECT * from {table_name} WHERE {field_name} LIKE ?"
        try: 
            conn = sqlite3.connect(self.session_db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql, [f"%{pattern}%"])
            records = cur.fetchall()
        except sqlite3.Error as e:
            psm_logger.debug(e)
            raise
        finally:
            if conn:
                conn.close()
        return records

    def get_objects_dict(self, table_name):
        sql = f"SELECT * from {table_name}"
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