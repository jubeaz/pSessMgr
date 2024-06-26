import typer
from typing_extensions import Annotated
from psm.logger import LOGLEVEL, set_logging_level
from psm.modules.domain import PSMDomain

app = typer.Typer()


@app.command()
def add(
    fqdn: Annotated[str, typer.Argument()],
    netbios: Annotated[str, typer.Option("--netbios", "-n", help="netbios name")] = None,
    sid: Annotated[str, typer.Option("--sid", "-s", help="SID")] = None,
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Create a new domain"""
    set_logging_level(debug)
    domain = PSMDomain(fqdn=fqdn)
    domain.add(netbios=netbios, sid=sid)
    print("[*] Domain added")

@app.command()
def update(
    fqdn: Annotated[str, typer.Argument()],
    netbios: Annotated[str, typer.Option("--netbios", "-n", help="netbios name")] = None,
    sid: Annotated[str, typer.Option("--sid", "-s", help="SID")] = None,
    dc_ip: Annotated[str, typer.Option("--dc", help="DC IP")] = None,
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Update a domain"""
    set_logging_level(debug)
    domain = PSMDomain(fqdn=fqdn)
    domain.update(netbios=netbios, sid=sid, dc_ip=dc_ip)
    print("[*] Domain updated")


@app.command()
def unset_dc(
    fqdn: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Update a domain"""
    set_logging_level(debug)
    domain = PSMDomain(fqdn=fqdn)
    domain.unset_dc()
    print("[*] Domain updated")


@app.command()
def activate(
    fqdn: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Activate a domain"""
    set_logging_level(debug)
    domain = PSMDomain(fqdn=fqdn)
    domain.activate()
    print("[*] Domain acteivated")

@app.command()
def target(
    fqdn: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Target a domain"""
    set_logging_level(debug)
    domain = PSMDomain(fqdn=fqdn)
    domain.target()
    print("[*] Domain targeted")

@app.command()
def delete(
    fqdn: Annotated[str, typer.Argument()],
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Delete a domain"""
    set_logging_level(debug)
    domain = PSMDomain(fqdn=fqdn)
    domain.delete()
    print("[*] Domain deleted")

@app.command()
def purge(
    debug: Annotated[LOGLEVEL, typer.Option("--debug", "-d", help="debug mode")] = LOGLEVEL.DEBUG
    ):
    """Delete all Domains"""
    set_logging_level(debug)
    domain = PSMDomain()
    domain.purge()
    print("[*] Domain purged")

@app.command()
def dump():
    """List domains"""
    set_logging_level(LOGLEVEL.INFO)
    domain = PSMDomain()
    domain.list()


if __name__ == "__main__":
    app()