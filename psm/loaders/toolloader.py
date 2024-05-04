from types import ModuleType
from importlib.machinery import SourceFileLoader
from os import listdir
from os.path import join
from os.path import dirname, exists, expanduser
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
            self.logger.fail(f"{module_path} missing the name variable")
            module_error = True
        elif not hasattr(module, "get_folder_locations") or not hasattr(module, "get_file_locations"):
            self.logger.fail(f"{module_path} missing the get_folder_locations/get_file_locations function")
            module_error = True

        return not module_error

    def get_tools(self):
        tools = {}
        path = join(dirname(psm.__file__), "tools")
        for tool in listdir(path):
            if tool[-3:] == ".py" and tool[:-3] != "__init__":
                 tool_path = join(path, tool)
                 tool_name = tool[:-3]
                 tools[tool_name] = {"path": tool_path}
        return tools

