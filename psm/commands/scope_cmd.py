import typer
from typing import Optional
from typing_extensions import Annotated
from psm.logger import psm_logger, LOGLEVEL, set_logging_level
from psm.modules.scope import PSMScope
from enum import Enum


app = typer.Typer()

class ComputerRole(str, Enum):
    dc = "dc"
    smb = "smb"
    mssql = "mssql"

@app.command()
def add(
    scope: Annotated[str, typer.Argument()],
    excluded: Annotated[bool, typer.Option("--excluded")] = False,
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Create a new Computer
    """
    set_logging_level(debug)
    scope = PSMScope(scope=scope)
    scope.add(excluded)
    print("[*] Scope added")

@app.command()
def delete(
    scope: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Delete a Computer
    """
    set_logging_level(debug)
    scope = PSMScope(scope=scope)
    scope.delete()
    print("[*] Scope deleted")

@app.command()
def list():
    """
    List computers
    """
    set_logging_level(LOGLEVEL.INFO)
    scope = PSMScope()
    scope.list()

if __name__ == "__main__":
    app()