import os
from psm.logger import psm_logger
import re
from pathlib import Path
from psm.config import arsenal_defaults_var_values, arsenal_cheat_search_path
from ast import literal_eval

class PSMTool():
    name = 'arsenal'
    #isolation_paths = [".arsenal.json"]
    isolation_paths = [".arsenal.json-psm"]
    user_config_path = '.arsenal.json'

    cheats_vars = {}
    cheat_search_path = None

    def get_isolation_paths(self):
        return self.isolation_paths

    def _search_for_vars(self, md_file_path):
        with open(md_file_path, 'r') as file:
            for arg_name in re.findall(r'<([^ <>]+)>', file.read(), re.DOTALL):
                if "|" in arg_name:  # Format <name|default_value>
                    arg_name, var = arg_name.split("|")[:2]
                    psm_logger.info(f"{arg_name} will not be added since defined with default value '{var}'")
                    continue
                if arg_name not in self.cheats_vars.keys():
                    self.cheats_vars[arg_name] = None

    def _apply_default_vars_value(self):
        # recupère la config
        for v in arsenal_defaults_var_values:
            if v[0] not in self.cheats_vars.keys():
                psm_logger.info(f"set {v[0]} to '{v[1]}'")
                self.cheats_vars[v[0]] = v[1]
            else:
                psm_logger.info(f"{v[0]} not found")

    def get_vars_with_value(self):
        vars = {}
        for var, value in  self.cheats_vars.items():
            if value:
                vars[var] = value
        return vars

    def load_arsenal_cheats_vars(self):
        self.cheats_vars = {}

        for path in Path(self.cheat_search_path).rglob('*.md'):
            #print(path)
            self._search_for_vars(path)
#        for k, v in self.cheats_vars.items():
#            print(f"var[{k}] = {v}")
        self._apply_default_vars_value()



    def computer_db(self):
        self.cheat_search_path = os.path.expanduser(arsenal_cheat_search_path)
        self.load_arsenal_cheats_vars()
        print(arsenal_cheat_search_path)
        raise RuntimeError('to do')

    def recomputer_db(self):
        raise RuntimeError('to do')
