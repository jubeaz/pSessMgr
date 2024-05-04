
import os
import typer
from typing_extensions import Annotated
from pathlib import Path
from typing import Optional
from psm.logger import psm_logger, LOGLEVEL, set_logging_level
from psm.modules.session import PSMSession
from psm.psmdb import PSMDB

app = typer.Typer()

def get_current_path():
    return os.getcwd()


@app.command()
def build(
    name: Annotated[str, typer.Argument()],
    path: Annotated[
        Path, 
        typer.Option(
            "--path",
            "-p",
            exists=True,
            writable=True,
            readable=True,
            default_factory=get_current_path,
            help="default current directory"
        )
    ],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Build a new pentest session
    """
    set_logging_level(debug)
    session = PSMSession(name=name,path=path)
    session.build()
    print("[*] session builded")


@app.command()
def list(debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG):
    """
    list pentest sessions
    """
    psm_db = PSMDB()
    psm_db.list_session()

@app.command()
def destroy(
    name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Destroy a pentest session
    """
    session = PSMSession(name=name)
    session.destroy()
    print("[*] session destoyed")

@app.command()
def activate(
    name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    activate a pentest session
    """
    session = PSMSession(name=name)
    session.activate()
    print("[*] session activated")

@app.command()
def deactivate(
    name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    activate a pentest session
    """
    session = PSMSession(name=name)
    session.deactivate()
    print("[*] session activated")


if __name__ == "__main__":
    app()