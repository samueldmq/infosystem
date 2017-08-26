import os
import importlib


def import_subsystems(path, package):
    dirs = [
        d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    modules = [importlib.import_module(package + '.' + m) for m in dirs]
    return [m.subsystem for m in modules if hasattr(m, 'subsystem')]


# TODO(samueldmq): import here or at destination directly ?
all = import_subsystems(
    os.path.dirname(os.path.realpath(__file__)), 'infosystem.subsystem')
