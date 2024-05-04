from os import mkdir
from os.path import exists
from shutil import copy, rmtree
from psm.paths import PSM_PATH, CONFIG_PATH, DEFAULT_CONFIG_PATH
from psm.logger import psm_logger
from psm.psmdb import PSMDB



def first_run_setup():
    try: 
        if not exists(PSM_PATH):
            psm_logger.info("First time use detected")
            psm_logger.info("Creating home directory structure")
            mkdir(PSM_PATH)

        if not exists(CONFIG_PATH):
            psm_logger.info("Copying default configuration file")
            copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)
        psm_db = PSMDB()
        psm_db.create_db()
        
    except Exception as e:
        psm_logger.error(e) 
        rmtree(PSM_PATH)
        raise
