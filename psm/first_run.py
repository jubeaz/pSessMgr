from os import mkdir
from os.path import exists
import shutil
from psm.paths import PSM_PATH, CONFIG_PATH, DATA_PATH, DEFAULT_CONFIG_PATH
from psm.logger import psm_logger



def first_run_setup(logger=psm_logger):
    try: 
        if not exists(PSM_PATH):
            logger.info("First time use detected")
            logger.info("Creating home directory structure")
            mkdir(PSM_PATH)

        if not exists(CONFIG_PATH):
            logger.info("Copying default configuration file")
            shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)
            from psm.psmdb import psm_db
    except: 
        rmtree(PSM_PATH)
        raise Exception()
