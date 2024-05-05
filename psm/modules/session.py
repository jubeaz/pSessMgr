import os
import configparser
import sys
import shutil
import importlib.util
from psm.loaders.toolloader import ToolLoader
from psm.logger import psm_logger
from shutil import rmtree, copytree
from psm.psmdb import PSMDB
from psm.config import session_template_folders, session_template_symlinks, session_template_tools, psm_config, CONFIG_PATH
from ast import literal_eval


class PSMSession:
    def __init__(self, name=None, path=None):
        self.psm_db = PSMDB()
        self.name = name
        self.base_dir = path
        self.session_id = None
        self.full_path = None
        self.tools_dir_paths = []
        if path:
            self.full_path = os.path.join(self.base_dir, self.name)

    def __str__(self):
        return f"{self.full_path}"

    def getactive(self):
        return psm_config.get("psm", "current_session")

    def isactive(self):
        return psm_config.get("psm", "current_session") == self.name

    def _get(self):
        self.session_id, self.full_path, self.tools_dir_paths = self.psm_db.get_session(self.name)

    def _create_fs(self):
        # create folders
        for f in session_template_folders:
            os.makedirs(os.path.join(self.full_path, f))
        psm_logger.debug("[*] folders created")
        # create symlins
        for s in session_template_symlinks:
            os.symlink(s[0], os.path.join(self.full_path, s[1]))
        self._copy_tools_data()
        psm_logger.debug("[*] symlinks created")
        psm_logger.info("[*] session created on filesystem")

    def _copy_tools_data(self):
        t_loader = ToolLoader()
        tools = t_loader.get_tools(session_template_tools)
        for t, v in tools.items():
            psm_logger.debug(f"[*] processing {t} tool")
            m = t_loader.load_tool(v["path"])
            psm_tool = m.PSMTool()
            paths = psm_tool.get_isolation_paths()
            for p in paths:
                src = os.path.join(os.path.expanduser('~'), p)
                dst = os.path.join(self.full_path, os.path.dirname(p))
                psm_logger.debug(f"mkdir {dst}")
                os.makedirs(dst, exist_ok=True)
                dst = os.path.join(self.full_path, p)
                psm_logger.debug(f"{dst} is file {os.path.isfile(p)}")
                if os.path.isdir(src):
                    psm_logger.debug(f"copy tree {src} to {dst}")
                    copytree(src, dst)
                else: 
                    psm_logger.debug(f"copy file {src} to {dst}")
                    shutil.copy(src, dst)
                self.tools_dir_paths.append(p)
        psm_logger.debug(f"notes {self.tools_dir_paths}")


    def _archive_tools_data(self):
        return

    def _link_tools_data(self):
        return

    def _check_creation(self):
        if os.path.exists(self.full_path):
            psm_logger.error(f"{self.full_path} already exist")
            raise RuntimeError("Session exist on fs")

    def build(self):
        self._check_creation()        
        try: 
            os.mkdir(self.full_path)
            psm_logger.debug(f"[*] {self.full_path} created")
            self._create_fs()

            session_id = self.psm_db.create_session(self.name, self.full_path, self.tools_dir_paths)
            psm_logger.debug("[*] db entry added as {}".format(session_id))
            psm_logger.info("[*] session created in database")
        except Exception as e:
            psm_logger.error(e)
            rmtree(self.full_path)
            raise

    def destroy(self):
        self._get()
        # if is active
        if self.session_id != -1:
            self.psm_db.delete_session(self.session_id)
        
        if  not os.path.exists(self.full_path):
            psm_logger.error(f"{self.full_path} does not exist on fs")
            raise RuntimeError("Project does not exist on FS")
        try: 
            print(self.full_path)
            rmtree(self.full_path)
        except Exception as e:
            print(self.full_path)
            psm_logger.error(f"[*] Exception {e}")
            psm_logger.error(f"[*] removing {self.full_path}")
        psm_logger.debug(f"[*] {self.full_path} destroyed")


    def _activate_tools_isolation(self):
        for p in self.tools_dir_paths:
            src = os.path.join(os.path.expanduser('~'), p)
            dst = os.path.join(self.full_path, p)
            # rename 
            psm_logger.debug(f"renaming {src} to {dst}.psm_save")
            os.rename(src, f"{src}.psm_save")
            # create symlink
            psm_logger.debug(f"creating symlink {dst} => {src}")
            os.symlink(dst, src)

    def activate(self):
        # check it exists
        # manage tools links in case new tools
        self._get()
        if self.isactive():
            psm_logger.info(f"[*] session {self.name} already active")
            return 
        if self.getactive() != "":
            psm_logger.error(f"[*] session {self.getactive()} is active please deactivate it")
            raise RecursionError("another session is active")
        #psm_logger.debug(f"debug {self.tools_dir_paths}")
        self._activate_tools_isolation()
        # rewrite config
        psm_config.set("psm", "current_session", self.name)
        with open(CONFIG_PATH, "w") as configfile:
            psm_config.write(configfile)

    def _deactivate_tools_isolation(self):
        for p in self.tools_dir_paths:
            src = os.path.join(os.path.expanduser('~'), p)
            dst = os.path.join(self.full_path, p)
            # remove symlink
            psm_logger.debug(f"removing symlink {src}")
            os.remove(src)
            # rename 
            psm_logger.debug(f"renaming {dst}.psm_save to {src}")
            os.rename(f"{src}.psm_save", src)

    def deactivate(self):
        self._get()
        if not self.isactive():
            psm_logger.info(f"[*] session {self.name} is not active")
            return 
        self._deactivate_tools_isolation()        
        # check it exists
        # manage tools links
        psm_config.set("psm", "current_session", "")
        with open(CONFIG_PATH, "w") as configfile:
            psm_config.write(configfile)
