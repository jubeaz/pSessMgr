import sqlite3 
from os.path import exists
from psm.paths import DB_PATH
from psm.logger import psm_logger
from tabulate import tabulate
import pandas as dp
from sqlalchemy import create_engine

#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)


class PSMDB():
    def __init__(self):
        self.db_path = DB_PATH

    def create_db(self):
        if not exists(DB_PATH):
            try: 
                conn = self.create_connection()
                cur = conn.cursor()
                cur.execute("""CREATE TABLE "sessions" (
                            "id" integer PRIMARY KEY,
                            "name" text,
                            "full_path" text,
                            UNIQUE(name)
                            )"""
                        )
                conn.commit()
                psm_logger.debug("batabase created")
            except sqlite3.Error as e:
                psm_logger.error(e)
                raise
            finally:
                conn.close()
        
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise
        return conn
    
    def create_session(self, name, full_path=None):
        sql = ''' INSERT INTO sessions(name, full_path)
                  VALUES(?, ?) '''
        if not full_path:
            raise RuntimeError("no path provided")
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql, [name, full_path])
        conn.commit()
        conn.close()
        return cur.lastrowid
    
    def list_session(self):
        conn = self.create_connection()
        tb_ss = dp.read_sql("SELECT * FROM sessions", conn)
        psm_logger.info(tabulate(tb_ss, showindex=False, headers=tb_ss.columns, tablefmt='grid'))

    def get_session(self, name):
        sql = ''' SELECT id, full_path FROM sessions 
                  WHERE name = ? '''
        if not name:
            raise RuntimeError("no name provided")
        try: 
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(sql, [name])
            record = cur.fetchone()
            session_id = record[0]
            full_path = record[1]
        except sqlite3.Error:
            session_id = -1
            full_path = None
        finally:
            if conn:
                conn.close()

        return session_id, full_path

    def delete_session(self, session_id):
        sql = ''' DELETE FROM sessions 
                  WHERE id = ? '''
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql, [session_id])
        conn.commit()
        conn.close()