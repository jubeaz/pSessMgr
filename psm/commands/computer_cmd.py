import typer
from typing import Optional
from typing_extensions import Annotated
from psm.logger import psm_logger, LOGLEVEL, set_logging_level
from psm.modules.computer import PSMComputer
from enum import Enum


app = typer.Typer()

class ComputerRole(str, Enum):
    dc = "dc"
    smb = "smb"
    mssql = "mssql"

@app.command()
def add(
    fqdn: Annotated[str, typer.Argument()],
    ip: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Create a new Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(fqdn=fqdn)
    computer.add(ip)
    print("[*] Computer added")

@app.command()
def update(
    fqdn: Annotated[str, typer.Argument()],
    ip: Annotated[str, typer.Option("--ip", "-i", help="ip address")] = None,
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Update a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(fqdn=fqdn)
    computer.update(netbios=netbios, sid=sid)
    print("[*] Computer updated")

@app.command()
def add_role(
    fqdn: Annotated[str, typer.Argument()],
    role: Annotated[ComputerRole, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Update a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(fqdn=fqdn)
    computer.add_role(role=role.value)
    print("[*] Computer updated")

@app.command()
def remove_role(
    fqdn: Annotated[str, typer.Argument()],
    role: Annotated[ComputerRole, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Update a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(fqdn=fqdn)
    computer.remove_role(role=role.value)
    print("[*] Computer updated")

@app.command()
def delete(
    fqdn: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Delete a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(fqdn=fqdn)
    computer.delete()
    print("[*] Computer builded")

@app.command()
def list():
    """
    List pentest sessions
    """
    set_logging_level(LOGLEVEL.INFO)
    computer = PSMComputer()
    computer.list()


if __name__ == "__main__":
    app()