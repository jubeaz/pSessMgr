import typer
import os
from rich import print

from psm.commands import session_cmd, domain_cmd, computer_cmd, scope_cmd, generator_cmd
from psm.lib.banner import small_banner, show_banner
from psm.logger import psm_logger, set_logging_level, DEFAULT_LOG_LEVEL
from psm.console import psm_console
from psm.first_run import first_run_setup
from psm.lib.functions import assert_active_session

from psm.psm_tests import my_tests

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode='rich',
    context_settings={'help_option_names': ['-h', '--help']},
    pretty_exceptions_show_locals=False
)


def default_callback():
    print("Running a users command")

callback=default_callback
app.add_typer(
    session_cmd.app,
    name="session",
    help="Manage sessions"
)


app.add_typer(
    domain_cmd.app,
    name="domain",
    help="Manage domains within a session"
)

app.add_typer(
    computer_cmd.app,
    name="computer",
    help="Manage computers within a session"
)

app.add_typer(
    scope_cmd.app,
    name="scope",
    help="Manage scopes within a session"
)

app.add_typer(
    generator_cmd.app,
    name="generator",
    help="Generate files"
)

@domain_cmd.app.callback()
@computer_cmd.app.callback()
@scope_cmd.app.callback()
@generator_cmd.app.callback()
def session_requiered_callback():
    assert_active_session()

def main():
    set_logging_level(DEFAULT_LOG_LEVEL)
#    my_tests()
    show_banner()
    first_run_setup()
    app(prog_name='psm')


if __name__ == "__main__":
    main()