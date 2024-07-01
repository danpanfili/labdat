import os
import copy
import importlib.util
import sys

class Module:
    def __init__(self, name='', args={}):
        self.__name__ = name
        self.SetArgs(args)

    def __repr__(self):
        return f'Module({self.__name__})'
    
    def __dir__(self):
        return [k for k in self.__dict__.keys() if not k.startswith('__')]
    
    def New(self, args={}):
        new = copy.deepcopy(self)
        new.SetArgs(args)
        return new
    
    def SetArgs(self, args):
        for key, val in args.items():
            setattr(self, key, val)

    def Import(self, path):
        # Create a new module
        spec = importlib.util.spec_from_file_location(self.__name__, path)
        module = importlib.util.module_from_spec(spec)

        # Add the module to sys.modules
        sys.modules[self.__name__] = module

        # Execute the module
        spec.loader.exec_module(module)

        # Add non-private attributes to the Module instance, excluding imports
        for name in dir(module):
            if not name.startswith('__') and name not in sys.modules:
                setattr(self, name, getattr(module, name))

def create_nested_classes(root_dir):
    instance = Module(root_dir)

    for current_dir, subdirs, files in os.walk(root_dir):
        relative_path = os.path.relpath(current_dir, root_dir)

        current_class = instance
        for subdir in relative_path.split(os.sep):
            if subdir != '.':
                if not hasattr(current_class, subdir):
                    setattr(current_class, subdir, Module(subdir))
                current_class = getattr(current_class, subdir)

        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = os.path.splitext(file)[0]
                module_path = os.path.join(current_dir, file)
                module_instance = Module(module_name)
                module_instance.Import(module_path)
                setattr(current_class, module_name, module_instance)

    return instance

# Access a Module object
labdat = create_nested_classes('labdat')