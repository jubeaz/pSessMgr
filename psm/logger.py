import logging
from rich.logging import RichHandler
from enum import Enum
from psm.console import psm_console

class LOGLEVEL(str, Enum):
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"

DEFAULT_LOG_LEVEL = LOGLEVEL.DEBUG


def set_logging_level(log_level):
    root_logger = logging.getLogger("root")

    if log_level == "DEBUG":
        psm_logger.setLevel(logging.DEBUG)
        root_logger.setLevel(logging.DEBUG)
    elif log_level == "ERROR":
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

        logging.getLogger("pypykatz").disabled = True
        logging.getLogger("minidump").disabled = True
        logging.getLogger("lsassy").disabled = True
        logging.getLogger("neo4j").setLevel(logging.ERROR)



# initialize the logger 
psm_logger = PSMAdapter()

