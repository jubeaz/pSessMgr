from types import ModuleType
from importlib.machinery import SourceFileLoader
from os import listdir
from os.path import join
from os.path import dirname
from psm.logger import psm_logger
import psm



class ToolLoader:
    tools = None

    def __init__(self):
        self.get_unfiltered_tools()

    def load_tool(self, tool_name):
        if tool_name not in self.tools:
            psm_logger.error(f"{tool_name} not in tools list")
            raise RuntimeError("Unsupported tool")
        
        loader = SourceFileLoader("PSMTool", self.tools[tool_name]["path"])
        tool = ModuleType(loader.name)
        loader.exec_module(tool)
        return tool

    def module_is_sane(self, module, module_path):
        module_error = False
        if not hasattr(module, "name"):
            psm_logger.error(f"{module_path} missing the name variable")
            module_error = True
        elif not hasattr(module, "get_isolation_paths"):
            psm_logger.error(f"{module_path} missing the get_isolation_paths function")
            module_error = True

        return not module_error

    def get_tools(self, filter_list=None):
        if filter_list is None:
            filter_list = []
        tools = self.get_unfiltered_tools()
        for t in tools.copy():
            if t not in filter_list:
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
            if tool.endswith(".py") and not tool.startswith("__init__"):
                tool_path = join(path, tool)
                tool_name = tool.removesuffix(".py")
                self.tools[tool_name] = {"path": tool_path}
                psm_logger.debug(f"{tool_name} added to tools list")
        return self.tools


psm_toolloader = ToolLoader()