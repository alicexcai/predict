import sys
import importlib.util

file_path = '/Users/alicecai/Desktop/csecon/PARAM/param/OFFICIAL/pages/simulation/doe.py'
module_name = 'simulation'

spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def bla(mod):
    print(dir(mod))
bla(module)

sys.modules[module_name] = module

# from pluginX import hello
doe()