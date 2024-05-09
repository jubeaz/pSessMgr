import typer
from typing import Optional
from typing_extensions import Annotated
from psm.logger import psm_logger, LOGLEVEL, set_logging_level
from psm.modules.scope import PSMScope
from psm.enums import FilterType

app = typer.Typer()

@app.command()
def add(
    scope: Annotated[str, typer.Argument()],
    action: Annotated[FilterType, typer.Option("--action", "-a")] = FilterType.allow,
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Create a new Scope
    """
    set_logging_level(debug)
    scope = PSMScope(scope=scope)
    scope.add(action)
    print("[*] Scope added")

@app.command()
def delete(
    scope: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Delete a Scope
    """
    set_logging_level(debug)
    scope = PSMScope(scope=scope)
    scope.delete()
    print("[*] Scope deleted")


@app.command()
def purge(
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Delete all Scopes
    """
    set_logging_level(debug)
    scope = PSMScope()
    scope.purge()
    print("[*] Scopes purged")

@app.command()
def list():
    """
    List Scopes
    """
    set_logging_level(LOGLEVEL.INFO)
    scope = PSMScope()
    scope.list()

if __name__ == "__main__":
    app()