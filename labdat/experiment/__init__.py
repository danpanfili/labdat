import os, importlib

subpackage_path             = os.path.dirname(__file__)
submodules                  = [f[:-3] for f in os.listdir(subpackage_path) if f.endswith('.py') and f != '__init__.py']
for module in submodules:   importlib.import_module(f".{module}", package=__name__)