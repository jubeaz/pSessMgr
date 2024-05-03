
import os
import typer
from typing_extensions import Annotated
from pathlib import Path
from typing import Optional
from psm.logger import psm_logger, LOGLEVEL, set_logging_level
from psm.modules.session import PSMSession


app = typer.Typer()

def get_current_path():
    return os.getcwd()


@app.command()
def create(
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
    Create a new pentest session
    """
    set_logging_level(debug)
    session = PSMSession(name=name,path=path,debug=debug)
    print(session)
    try:
        session.create()
    except:
        raise typer.Abort()

@app.command()
def destroy(
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
    Destroy a pentest session
    """
    session = PSMSession(name=name,path=path,debug=debug)
    print(session)
    try:
        session.destroy()
    except:
        raise typer.Abort()   

@app.command()
def activate(debug: Annotated[Optional[bool], typer.Option("--debug", "-d", help="debug mode")] = False):
    """
    activate a pentest session
    """
    return

@app.command()
def close(debug: Annotated[Optional[bool], typer.Option("--debug", "-d", help="debug mode")] = False):
    """
    close a pentest session
    """
    return


if __name__ == "__main__":
    app()