import os
import configparser
import sys
import shutil
import importlib.util
from psm.loaders.toolloader import psm_toolloader
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
        self.tools = []
        self.tools_dir_paths = []
        if path:
            self.full_path = os.path.join(self.base_dir, self.name)

    def __str__(self):
        return f"{self.full_path}"

    def getactive(self):
        return psm_config.get("psm", "current_session")

    def isactive(self):
        return psm_config.get("psm", "current_session") == self.name

    def get(self):
        self.session_id, self.full_path, self.tools, self.tools_dir_paths = self.psm_db.get_session(self.name)

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

    def _copy_tool_data(self, tool_ame):
        psm_logger.debug(f"[*] processing {tool_ame} tool")
        m = psm_toolloader.load_tool(tool_ame)
        psm_tool = m.PSMTool()
        paths_i = psm_tool.get_isolation_paths(self.full_path)
        for path_i in paths_i:
            src =path_i["src"]
            dst = path_i["dst"]
            psm_logger.debug(f"mkdir {os.path.dirname(dst)}")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            psm_logger.debug(f"{src} is file {os.path.isfile(src)}")
            if os.path.isdir(src):
                psm_logger.debug(f"copy tree {src} to {dst}")
                copytree(src, dst)
            else: 
                psm_logger.debug(f"copy file {src} to {dst}")
                shutil.copy(src, dst)
            self.tools_dir_paths.append(path_i)

    def _copy_tools_data(self):
        tools = psm_toolloader.get_tools(session_template_tools)
        for tool_name in tools.keys():
            self._copy_tool_data(tool_name)
            self.tools.append(tool_name)
        psm_logger.debug(f"notes {self.tools_dir_paths}")

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

            session_id = self.psm_db.create_session(self.name, 
                                                    self.full_path,
                                                    self.tools, 
                                                    self.tools_dir_paths,
                                                    )
            psm_logger.debug("[*] db entry added as {}".format(session_id))
            psm_logger.info("[*] session created in database")
        except Exception as e:
            psm_logger.error(e)
            rmtree(self.full_path)
            raise

    def destroy(self):
        self.get()
        # if is active
        if self.isactive():
            psm_logger.error(f"{self.name} is active")
            raise RuntimeError("Can't delete active session")   
        if self.session_id != -1:
            self.psm_db.delete_session(self.session_id)
     
        if  not os.path.exists(self.full_path):
            psm_logger.error(f"{self.full_path} does not exist on fs")
            raise RuntimeError("Session does not exist on FS")
        try: 
            print(self.full_path)
            rmtree(self.full_path)
        except Exception as e:
            print(self.full_path)
            psm_logger.error(f"[*] Exception {e}")
            psm_logger.error(f"[*] removing {self.full_path}")
        psm_logger.debug(f"[*] {self.full_path} destroyed")


    def _isolate_tool(self, path_i):
        # rename 
        psm_logger.debug(f"renaming {path_i["src"]} to {path_i["src"]}.psm_save")
        os.rename(path_i["src"], f"{path_i["src"]}.psm_save")
        # create symlink
        psm_logger.debug(f"creating symlink {path_i["dst"]} => {path_i["src"]}")
        os.symlink(path_i["ds"], path_i["src"])

    def _activate_tools_isolation(self):
        for path_i in self.tools_dir_paths:
            self._isolate_tool(path_i)


    def activate(self):
        # check it exists
        # manage tools links in case new tools
        self.get()
        if self.session_id == -1:
            psm.logger.error(f"Session {name} not found in db")
            raise RuntimeError("Session not found in db")
        if self.isactive():
            psm_logger.info(f"[*] session {self.name} already active")
            return 
        if self.getactive() != "":
            psm_logger.error(f"[*] session {self.getactive()} is active please deactivate it")
            raise RuntimeError("another session is active")
        self._activate_tools_isolation()
        # rewrite config
        psm_config.set("psm", "current_session", self.name)
        with open(CONFIG_PATH, "w") as configfile:
            psm_config.write(configfile)

    def _unisolate_tool(self, path_i):
        src = path_i["src"]
        dst = path_i["dst"]
        # remove symlink
        psm_logger.debug(f"removing symlink {src}")
        os.remove(src)
        # rename 
        psm_logger.debug(f"renaming {dst}.psm_save to {src}")
        os.rename(f"{src}.psm_save", src)


    def _deactivate_tools_isolation(self):
        for p in self.tools_dir_paths:
            self._unisolate_tool(p)

    def deactivate(self):
        self.get()
        if self.session_id == -1:
            psm.logger.error("Session not found in db")
            raise RuntimeError("Session not found in db")
        if not self.isactive():
            psm_logger.info(f"[*] session {self.name} is not active")
            return 
        self._deactivate_tools_isolation()        
        # check it exists
        # manage tools links
        psm_config.set("psm", "current_session", "")
        with open(CONFIG_PATH, "w") as configfile:
            psm_config.write(configfile)

    def add_tool(self, tool_name):
        tools = psm_toolloader.get_unfiltered_tools()
        if tool_name not in tools.keys():
            psm_logger.error(f"[*] {tool_name} not supported")
            raise RuntimeError("Unsupported tool")
        self.get()
        if self.session_id == -1:
            psm.logger.error("Session not found in db")
            raise RuntimeError("Session not found in db")
        if tool_name in self.tools:
            psm_logger.error(f"[*] {tool_name} already isolated in session")
            raise RuntimeError("Already isolated tool")
        self._copy_tool_data(tool_name)
        self.tools.append(tool_name)
        # update db
        self.psm_db.update_session(self.session_id, self.tools, self.tools_dir_paths)
        if self.isactive():
            psm_logger.info(f"[*] isolating {tool_name} in {self.name}")
            m = psm_toolloader.load_tool(tool_name)
            psm_tool = m.PSMTool()
            paths = psm_tool.get_isolation_paths()
            for path in paths:
                self._isolate_tool(path)


