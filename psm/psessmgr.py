import typer
from psm.commands import session, domain
from psm.scripts.banner import small_banner, show_banner
from psm.logger import psm_logger, set_logging_level
from psm.console import psm_console
from psm.first_run import first_run_setup
import os
from rich import print


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
    session.app,
    name="session",
    help="Manage sessions"
)

#
#app.add_typer(
#    domain.app,
#    name="domain",
#    help="Manage domain within a project"
#)
#




def main():
    show_banner()
    set_logging_level('DEBUG')
    first_run_setup(psm_logger)
    #small_banner()
#    project_name = None
#    if "PSM_CURREN_PROJECT" in os.environ:
#        project_name = os.environ.get('PSM_CURREN_PROJECT')
#    print(f'project: [bold red]{project_name} [/bold red] :boom:')

    app(prog_name='psm')


if __name__ == "__main__":
    main()