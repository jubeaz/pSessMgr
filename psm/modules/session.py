import os
from psm.logger import psm_logger
from shutil import rmtree
#from psm.config import PROJECT_DIRS, PROJECT_lINKS

PROJECT_DIRS=[]
PROJECT_lINKS=[]

class PSMSession:
    def __init__(self, name=False, path=False, debug=False):
        self.name = name
        self.base_dir = path
        self.debug = debug

    def __str__(self):
        return f"{self.base_dir}/{self.name}"


    def create(self):
        full_path = os.path.join(self.base_dir, self.name)
        if os.path.exists(full_path):
            psm_logger.error(f"{full_path} already exist")
            raise Exception()
        try: 
            os.mkdir(full_path)
        except:
            psm_logger.error(f"[*] creating {full_path}")
        psm_logger.debug(f"[*] {full_path} created")
        try:
            for dir in PROJECT_DIRS:
                os.makedirs(os.path.join(full_path, dir))
                psm_logger.debug(f"[*] creating dir {os.path.join(full_path, dir)}")
            psm_logger.debug(f"[*] sub folders created")
            for link in PROJECT_lINKS:
                os.symlink(link[0], os.path.join(full_path, link[1]))
                psm_logger.debug(f"[*] linking {link[0]} to {os.path.join(full_path, link[1])}")
            psm_logger.debug(f"[*] links  created")
        except:
            self.destroy()
            psm_logger.error(f"[*] content creation error roll-back")

    def destroy(self):
        full_path = os.path.join(self.base_dir, self.name)
        if not os.path.exists(full_path):
            psm_logger.error(f"{full_path} not present")
            raise Exception()
        try: 
            rmtree(full_path)
        except:
            psm_logger.error(f"[*] removing {full_path}")
        psm_logger.debug(f"[*] {full_path} destroyed")