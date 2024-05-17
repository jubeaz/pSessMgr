import typer
from typing_extensions import Annotated
from psm.logger import LOGLEVEL, set_logging_level
from psm.modules.generator import PSMGenerator


app = typer.Typer()

@app.command()
def export_etc_hosts(
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Generate a /etc/hosts file"""
    set_logging_level(debug)
    generator = PSMGenerator()
    generator.export_etc_hosts()
    print("[*] file generated")

@app.command()
def export_ip(
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Generate a /etc/hosts file"""
    set_logging_level(debug)
    generator = PSMGenerator()
    generator.export_ip_list()
    print("[*] file generated")

@app.command()
def export_fqdn(
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Generate a /etc/hosts file"""
    set_logging_level(debug)
    generator = PSMGenerator()
    generator.export_fqdn_list()
    print("[*] file generated")

@app.command()
def export_etc_krb5_conf(
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Generate a /etc/hosts file"""
    set_logging_level(debug)
    generator = PSMGenerator()
    generator.export_etc_krb5_conf()
    print("[*] file generated")
