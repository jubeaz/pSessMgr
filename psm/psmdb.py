import sqlite3 
from os.path import exists
from psm.paths import DB_PATH
from psm.logger import psm_logger
from tabulate import tabulate
import pandas as pd
from ast import literal_eval

class PSMDB:
    def __init__(self):
        self.db_path = DB_PATH

    def create_db(self):
        if exists(DB_PATH):
            return
        try: 
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute("""CREATE TABLE "sessions" (
                        "id" integer PRIMARY KEY,
                        "name" text,
                        "full_path" text,
                        "tools" text,
                        "tools_dir_paths" text,
                        UNIQUE(name)
                        )"""
                    )
            conn.commit()
            psm_logger.debug("batabase created")
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise
        finally:
            if conn:
                conn.close()
        
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise
        return conn
    
    def create_session(self, name, full_path, tools, tools_dir_paths):
        sql = """ INSERT INTO sessions(name, full_path, tools, tools_dir_paths)
                  VALUES(?, ?, ?, ?) """
        if not full_path:
            raise RuntimeError("no path provided")
        try: 
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(sql, [name, full_path, repr(tools), repr(tools_dir_paths)])
            conn.commit()
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise RuntimeError("create_sesssion_error") from None
        finally:
            psm_logger.debug(f" db creation of {name}, {full_path}, {tools_dir_paths}")
            if conn:
                conn.close()

        return cur.lastrowid
    
    def list_session(self):
        conn = self.create_connection()
        tb_ss = pd.read_sql("SELECT * FROM sessions", conn)
        psm_logger.info(tabulate(tb_ss, showindex=False, headers=tb_ss.columns, tablefmt="grid"))

    def get_session(self, name):
        sql = """ SELECT id, full_path, tools, tools_dir_paths FROM sessions 
                  WHERE name = ? """
        if not name:
            raise RuntimeError("no name provided")
        try: 
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(sql, [name])
            record = cur.fetchone()
            session_id = record[0]
            full_path = record[1]
            tools = literal_eval(record[2])
            tools_dir_paths = literal_eval(record[3])
        except sqlite3.Error:
            session_id = -1
            full_path = None
            tools = None
            tools_dir_paths = None
            psm_logger.debug(f"{name} session not found in db")
        finally:
            if conn:
                conn.close()

        return session_id, full_path, tools, tools_dir_paths

    def update_session(self, session_id, tools, tools_dir_paths):
        sql = """ UPDATE sessions 
                    SET tools = ?, tools_dir_paths = ?
                  WHERE id = ? """
        try: 
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(sql, [repr(tools), repr(tools_dir_paths), session_id])
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise

    def delete_session(self, session_id):
        sql = """ DELETE FROM sessions 
                  WHERE id = ? """
        try: 
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(sql, [session_id])
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise