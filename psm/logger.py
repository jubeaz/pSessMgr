import logging
import os
from rich.logging import RichHandler
from rich.console import Console
from enum import Enum
from psm.console import psm_console

class LOGLEVEL(str, Enum):
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"

DEFAULT_LOG_LEVEL = LOGLEVEL.DEBUG
#OBJ_EXTRA_FMT = {
#    "markup": True,
#    "highlighter": False
#}


def set_logging_level(log_level):
    root_logger = logging.getLogger("root")

    if log_level == 'DEBUG':
        psm_logger.setLevel(logging.DEBUG)
        root_logger.setLevel(logging.DEBUG)
    elif log_level == 'ERROR':
        psm_logger.setLevel(logging.ERROR)
        root_logger.setLevel(logging.ERROR)
    else:
        psm_logger.setLevel(logging.INFO)
        root_logger.setLevel(logging.INFO) 



class PSMAdapter(logging.LoggerAdapter):
    def __init__(self, extra=None):
        logging.basicConfig(
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(
                console=psm_console,
                rich_tracebacks=True,
                tracebacks_show_locals=False
            )],
        )
        self.logger = logging.getLogger("psm")
        self.extra = extra
        self.output_file = None

        #logging.getLogger("pypykatz").disabled = True
        #logging.getLogger("minidump").disabled = True
        #logging.getLogger("lsassy").disabled = True
        #logging.getLogger("neo4j").setLevel(logging.ERROR)



def prep_logs():
    home = os.path.expanduser('~')
    save_dir = f'{(home)}/.psm'
    logs_dir = f'{save_dir}/logs'
    loot_dir = f'{logs_dir}/loot'
    csv_dir = f'{logs_dir}/csvs'
    json_dir = f'{logs_dir}/json'
    db_dir = f'{logs_dir}/db'
    #if not os.path.isdir(save_dir):
    #    logger.info("[!] First time use detected.")
    #    logger.info(f"[!]  data will be saved to {save_dir}")
    #    os.mkdir(save_dir)
    #if not os.path.isdir(logs_dir):
    #    os.mkdir(logs_dir)
    #if not os.path.isdir(loot_dir):
    #    os.mkdir(loot_dir)
    #if not os.path.isdir(csv_dir):
    #    os.mkdir(csv_dir)
    #if not os.path.isdir(json_dir):
    #    os.mkdir(json_dir)
    return logs_dir



# initialize the logger 
psm_logger = PSMAdapter()

