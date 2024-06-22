import typer

from psm.logger import psm_logger, set_logging_level, LOGLEVEL
from psm.config import current_session


def assert_active_session():
    set_logging_level(LOGLEVEL.INFO)
    if not current_session:
        psm_logger.error("No active session")
        raise typer.Abort
