from os import mkdir
from os.path import exists
from shutil import copy, rmtree
from psm.paths import PSM_PATH, CONFIG_PATH, DEFAULT_CONFIG_PATH
from psm.logger import psm_logger, set_logging_level, DEFAULT_LOG_LEVEL
from psm.psmdb import PSMDB



def first_run_setup():
    try: 
        set_logging_level(DEFAULT_LOG_LEVEL)
        if not exists(PSM_PATH):
            psm_logger.debug("First time use detected")
            psm_logger.debug("Creating home directory structure")
            mkdir(PSM_PATH)

        if not exists(CONFIG_PATH):
            psm_logger.debug("Copying default configuration file")
            copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)
        psm_db = PSMDB()
        psm_db.create_db()
        
    except Exception as e:
        psm_logger.error(e) 
        rmtree(PSM_PATH)
        raise
