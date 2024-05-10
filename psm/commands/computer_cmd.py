import typer
from typing import Optional
from typing_extensions import Annotated
from psm.logger import psm_logger, LOGLEVEL, set_logging_level
from psm.modules.computer import PSMComputer
from psm.enums import ComputerRole
from pathlib import Path


app = typer.Typer()

@app.command()
def add(
    ip: Annotated[str, typer.Argument()],
    short_name: Annotated[str, typer.Option("--short", "-s", help="short name")] = None,    
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Create a new Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(ip=ip)
    computer.add(short_name)
    print("[*] Computer added")

@app.command()
def update(
    ip: Annotated[str, typer.Argument()],
    short_name: Annotated[str, typer.Option("--short", "-s", help="short name")] = None,    
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Update a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(ip=ip)
    computer.update(short_name=short_name)
    print("[*] Computer updated")

@app.command()
def add_fqdn(
    ip: Annotated[str, typer.Argument()],
    fqdn: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Add a FQDN to a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(ip=ip)
    computer.add_fqdn(fqdn)
    print("[*] FQDN added updated")

@app.command()
def remove_fqdn(
    ip: Annotated[str, typer.Argument()],
    fqdn: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Remove a FQDN to a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(ip=ip)
    computer.remove_fqdn(fqdn)
    print("[*] FQDN removed")

@app.command()
def add_role(
    ip: Annotated[str, typer.Argument()],
    role: Annotated[ComputerRole, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Add a role to a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(ip=ip)
    computer.add_role(role=role.value)
    print("[*] Role added updated")

@app.command()
def remove_role(
    ip: Annotated[str, typer.Argument()],
    role: Annotated[ComputerRole, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Remove a role to a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(ip=ip)
    computer.remove_role(role=role.value)
    print("[*] Role removed")

@app.command()
def delete(
    ip: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Delete a Computer
    """
    set_logging_level(debug)
    computer = PSMComputer(ip=ip)
    computer.delete()
    print("[*] Computer deleted")

@app.command()
def purge(
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    Delete all Computers
    """
    set_logging_level(debug)
    computer = PSMComputer()
    computer.purge()
    print("[*] Computers purged")

@app.command()
def list():
    """
    List computers
    """
    set_logging_level(LOGLEVEL.INFO)
    computer = PSMComputer()
    computer.list()

@app.command()
def import_nmap(
    file: Annotated[
        Path, 
        typer.Argument(
            exists=True,
            writable=True,
            readable=True,
            help="namp xml output file"
        )
    ],
    dry_run: Annotated[bool, typer.Option("--dry-run", help="dry_run mode")] = False,
    store_details: Annotated[bool, typer.Option("--store-details", "-s", help="import scan details")] = False,
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """
    import computers from nmap
    """
    set_logging_level(LOGLEVEL.INFO)
    computer = PSMComputer()
    computer.nmap_import(file_path=file, dry_run=dry_run, store_details=store_details)

if __name__ == "__main__":
    app()