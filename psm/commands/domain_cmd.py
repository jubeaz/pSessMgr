import typer
from psm.logger import psm_logger, LOGLEVEL, set_logging_level

app = typer.Typer()


@app.command()
def create(name: str):
    """
    Create a new domain
    """
    raise RuntimeError("todo")


if __name__ == "__main__":
    app()