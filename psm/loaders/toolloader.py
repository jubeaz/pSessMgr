from types import ModuleType
from importlib.machinery import SourceFileLoader
from os import listdir
from os.path import join
from os.path import dirname, exists, expanduser
from psm.logger import psm_logger
import psm

class ToolLoader:
    def load_tool(self, tool_path):
        loader = SourceFileLoader("PSMTool", tool_path)
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


    def get_tools(self, list=[]):
        tools = {}
        path = join(dirname(psm.__file__), "tools")
        for tool in listdir(path):
            if tool[-3:] == ".py" and tool[:-3] != "__init__" and  tool[:-3] in list:
                tool_path = join(path, tool)
                tool_name = tool[:-3]
                tools[tool_name] = {"path": tool_path}
                psm_logger.debug(f"{tool_name} will be added to tools list")
            else:
                psm_logger.debug(f"{tool[:-3]} will NOT to tools list")     
        return tools

