import os
import configparser
from os.path import join as path_join
from psm.paths import PSM_PATH, DEFAULT_CONFIG_PATH, CONFIG_PATH
from psm.first_run import first_run_setup
from psm.logger import psm_logger
from ast import literal_eval

psm_default_config = configparser.ConfigParser()
psm_default_config.read(DEFAULT_CONFIG_PATH)

psm_config = configparser.ConfigParser()
psm_config.read(CONFIG_PATH)

if "psm" not in psm_config.sections():
    first_run_setup()
    psm_config.read(CONFIG_PATH)

# Check if there are any missing options in the config file
for section in psm_default_config.sections():
    for option in psm_default_config.options(section):
        if not psm_config.has_option(section, option):
            psm_logger.display(f"Adding missing option '{option}' in config section '{section}' to psm.conf")
            psm_config.set(section, option, psm_default_config.get(section, option))

            with open(path_join(PSM_PATH, "psm.conf"), "w") as config_file:
                psm_config.write(config_file)

# THESE OPTIONS HAVE TO EXIST IN THE DEFAULT CONFIG FILE
current_session = psm_config.get("psm", "current_session", fallback="")

session_template_folders = literal_eval(psm_config.get("session_template", "folders", fallback=[]))
session_template_symlinks = literal_eval(psm_config.get("session_template", "symlinks", fallback=[]))

sqlmap_config = psm_config.get("tools", "sqlmap", fallback=".local.share.sqlmap")
john_config = psm_config.get("tools", "john", fallback=".john")
nxc_config = psm_config.get("tools", "nxc", fallback=".nxc")
jwt_tools_config = psm_config.get("tools", "jwt_tools", fallback=".jwt_tools")
hashcat_config = psm_config.get("tools", "hashcat", fallback=".local/share/hashcat")
tplmap_config = psm_config.get("tools", "tplmap", fallback=".tplmap")
arsenal_config = psm_config.get("tools", "arsenal", fallback=".arsenal.json")
tmuxinator_config = psm_config.get("tools", "tmuxinator", fallback=".tmux-pentest.yml")