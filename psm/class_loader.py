
import os
import sys
import inspect
import importlib.util
from psm.loaders.toolloader import ToolLoader
from psm.logger import psm_logger



def load_modules_from_path(path):
   """
   Import all modules from the given directory
   """
   # Check and fix the path
   if path[-1:] != '/':
       path += '/'

   # Get a list of files in the directory, if the directory exists
   if not os.path.exists(path):
        raise OSError("Directory does not exist: %s" % path)

   # Add path to the system path
   sys.path.append(path)
   # Load all the files in path
   for f in os.listdir(path):
       # Ignore anything that isn't a .py file
       if len(f) > 3 and f[-3:] == '.py':
           modname = f[:-3]
           # Import the module
           __import__(modname, globals(), locals(), ['*'])

def load_class_from_name(fqcn):
    # Break apart fqcn to get module and classname
    paths = fqcn.split('.')
    modulename = '.'.join(paths[:-1])
    classname = paths[-1]
    # Import the module
    __import__(modulename, globals(), locals(), ['*'])
    # Get the class
    cls = getattr(sys.modules[modulename], classname)
    # Check cls
    if not inspect.isclass(cls):
       raise TypeError("%s is not a class" % fqcn)
    # Return class
    return cls

def class_loader_old():
    tool = "nxc"
    t_loader = ToolLoader()
    tools = t_loader.get_tools()
    for t, v in tools.items():
        print(f"{t}")
        print(f"{v}")
        spec = importlib.util.spec_from_file_location("PSMTool", v["path"])
        foo = importlib.util.module_from_spec(spec)
        sys.modules["psm.tools.PSMTool"] = foo
        spec.loader.exec_module(foo)
        psm_tool = foo.PSMTool()
        print(psm_tool.get_locations())


def class_loader():
    tools_path = []
    t_loader = ToolLoader()
    tools = t_loader.get_tools()
    for t, v in tools.items():
        m = t_loader.load_tool(v["path"])
        psm_tool = m.PSMTool()
        tools_path.append(psm_tool.get_locations())
    print(tools_path)

    