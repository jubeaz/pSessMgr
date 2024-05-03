#from sqlalchemy import create_engine
import sqlite3 
from os.path import exists
from psm.paths import DB_PATH
from psm.logger import psm_logger

#def create_db_engine(db_path):def create_db_engine(db_path):
#    return create_engine(f"sqlite:///{db_path}", isolation_level="AUTOCOMMIT", future=True)

sql_table_session_template = """CREATE TABLE "session_template" (
                                    "id" integer PRIMARY KEY,
                                    "name" text,
                                    "template" integer
                                )"""

sql_table_session = """CREATE TABLE "sessions" (
                            "id" integer PRIMARY KEY,
                            "name" text,
                            "path" text,
                            "template_id" integer,
                            FOREIGN KEY(template_id) REFERENCES session_template(id)
                        )"""

class PSMDB():
    def __init__(self):
        self.db_path = DB_PATH
        if not exists(DB_PATH):
            con = self.create_connection()
            psm_logger.info("creating bd")
            self.create_table(sql_table_session_template)
            self.create_table(sql_table_session)
            con.commit()
            con.close()
        
    def create_connection(self):
        con = None
        try:
            con = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise Exception()
        return con
        
    def create_table(self, sql_request):
        try:
            c = self.create_connection().cursor()
            c.execute(sql_request)
        except sqlite3.Error as e:
            psm_logger.error(e)
            raise Exception()

    def import_template(self):
        

psm_db = PSMDB()         
