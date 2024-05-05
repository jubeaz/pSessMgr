from types import ModuleType
from importlib.machinery import SourceFileLoader
from os import listdir
from os.path import join
from os.path import dirname, exists, expanduser
from psm.logger import psm_logger
import psm



class ToolLoader:
    tools = None

    def __init__(self):
        self.get_unfiltered_tools()

    def load_tool(self, tool_name):
        if tool_name not in self.tools.keys():
            psm_logger.error(f"{tool_name} not in tools list")
            raise RuntimeError("Unsupported tool")
        
        loader = SourceFileLoader("PSMTool", self.tools[tool_name]["path"])
        tool = ModuleType(loader.name)
        loader.exec_module(tool)
        return tool

#    def load_tool(self, tool_path):
#        loader = SourceFileLoader("PSMTool", tool_path)
#        tool = ModuleType(loader.name)
#        loader.exec_module(tool)
#        return tool

    def module_is_sane(self, module, module_path):
        module_error = False
        if not hasattr(module, "name"):
            psm_logger.error(f"{module_path} missing the name variable")
            module_error = True
        elif not hasattr(module, "get_isolation_paths"):
            psm_logger.error(f"{module_path} missing the get_isolation_paths function")
            module_error = True

        return not module_error

    def get_tools(self, list=[]):
        tools = self.get_unfiltered_tools()
        for t in tools.copy().keys():
            if t not in list:
                psm_logger.debug(f"{t} filtred out")
                del tools[t]
        return tools

##
# IMPROVE:
#   load each tool (psm_tool = m.PSMTool())
#   use a function get_name() instead of the filename
##

    def get_unfiltered_tools(self):
        if self.tools is not None:
            return self.tools
        self.tools = {}
        path = join(dirname(psm.__file__), "tools")
        for tool in listdir(path):
            if tool[-3:] == ".py" and tool[:-3] != "__init__":
                tool_path = join(path, tool)
                tool_name = tool[:-3]
                self.tools[tool_name] = {"path": tool_path}
                psm_logger.debug(f"{tool_name} added to tools list")
        return self.tools


psm_toolloader = ToolLoader()