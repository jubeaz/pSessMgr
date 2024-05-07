import sqlite3 
from os.path import exists
from psm.logger import psm_logger
from tabulate import tabulate
import pandas as dp
from sqlalchemy import create_engine
from ast import literal_eval


class PSMSessionDB:
    session_db_path = None

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
