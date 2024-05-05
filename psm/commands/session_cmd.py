
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
    print("[*] Session builded")

@app.command()
def list():
    """
    List pentest sessions
    """
    set_logging_level(LOGLEVEL.INFO)
    psm_db = PSMDB()
    psm_db.list_session()
    print("[*] Session builded")

@app.command()
def destroy(
    name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Destroy an inactive pentest session
    """
    session = PSMSession(name=name)
    session.destroy()
    print("[*] Session destoyed")

@app.command()
def activate(
    name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Activate a pentest session
    """
    session = PSMSession(name=name)
    session.activate()
    print("[*] Session activated")

@app.command()
def deactivate(
    name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Deactivate a pentest session
    """
    session = PSMSession(name=name)
    session.deactivate()
    print("[*] Session deactivated")


@app.command()
def add(
    name: Annotated[str, typer.Argument()],
    tool_name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Add a tool to a pentest session (with activation if session is active)
    """
    session = PSMSession(name=name)
    session.add_tool(tool_name)
    print("[*] Tool added")

@app.command()
def remove(
    name: Annotated[str, typer.Argument()],
    tool_name: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Remove a tool to a pentest session
    """
    raise RuntimeError("todo")

if __name__ == "__main__":
    app()