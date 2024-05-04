import os
import configparser
from psm.logger import psm_logger
from shutil import rmtree
from psm.psmdb import PSMDB
from psm.config import session_template_folders, session_template_symlinks, psm_config, CONFIG_PATH
from ast import literal_eval


class PSMSession:
    def __init__(self, name=None, path=None):
        self.psm_db = PSMDB()
        self.name = name
        self.base_dir = path
        self.session_id = None
        self.full_path = None
        if path:
            self.full_path = os.path.join(self.base_dir, self.name)

    def __str__(self):
        return f"{self.full_path}"

    def _get(self):
        self.session_id, self.full_path = self.psm_db.get_session(self.name)

    def _create_fs(self):
        # create folders
        for f in session_template_folders:
            os.makedirs(os.path.join(self.full_path, f))
        psm_logger.debug("[*] folders created")

        # create symlins
        for s in session_template_symlinks:
            os.symlink(s[0], os.path.join(self.full_path, s[1]))
        psm_logger.debug("[*] symlinks created")
        psm_logger.info("[*] session created on filesystem")

    def _check_creation(self):
        if os.path.exists(self.full_path):
            psm_logger.error(f"{self.full_path} already exist")
            raise RuntimeError("Project exist")

    def build(self):
        self._check_creation()        
        try: 
            os.mkdir(self.full_path)
            psm_logger.debug(f"[*] {self.full_path} created")
            self._create_fs()
            # create db_entry
            session_id = self.psm_db.create_session(self.name, self.full_path)
            psm_logger.debug("[*] db entry added as {}".format(session_id))
            psm_logger.info("[*] session created in database")
        except Exception as e:
            psm_logger.error(e)
            rmtree(self.full_path)
            raise



    def destroy(self):
        self._get()
        if self.session_id != -1:
            self.psm_db.delete_session(self.session_id)
        
        if  not os.path.exists(self.full_path):
            psm_logger.error(f"{self.full_path} does not exist")
            raise RuntimeError("Project does not exist on FS")
        try: 
            print(self.full_path)
            rmtree(self.full_path)
        except Exception as e:
            print(self.full_path)
            psm_logger.error(f"[*] Exception {e}")
            psm_logger.error(f"[*] removing {self.full_path}")
        psm_logger.debug(f"[*] {self.full_path} destroyed")

    def activate(self):

        # check it exists

        # manage tools links in case new tools
        
        if psm_config.get("psm", "current_session") == self.name:
            psm_logger.info(f"[*] session {self.name} already active")
            return 
        # rewrite config
        psm_config.set("psm", "current_session", self.name)
        with open(CONFIG_PATH, "w") as configfile:
            psm_config.write(configfile)

    def deactivate(self):
        if psm_config.get("psm", "current_session") != self.name:
            psm_logger.info(f"[*] session {self.name} is not active")
            return 
        # check it exists

        # manage tools links

        psm_config.set("psm", "current_session", self.name)
        with open(CONFIG_PATH, "w") as configfile:
            psm_config.write(configfile)
