import os
import importlib

# Get the current directory of the subpackage
subpackage_path = os.path.dirname(__file__)

# Get a list of all Python files in the subpackage
submodules = [f[:-3] for f in os.listdir(subpackage_path) if f.endswith('.py') and f != '__init__.py']

# Import all modules dynamically
for module in submodules:
    importlib.import_module(f".{module}", package=__name__)