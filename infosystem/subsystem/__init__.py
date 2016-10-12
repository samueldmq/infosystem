import importlib
import os


def import_subsystems(path):
    dirs = [d for d in os.listdir('/'.join(path)) if os.path.isdir(os.path.join('/'.join(path), d))]
    modules = [importlib.import_module('.'.join(path + [m])) for m in dirs]
    return [m.subsystem for m in modules if hasattr(m, 'subsystem')]

# TODO(samueldmq): import here or at destination directly ?
all = import_subsystems(['infosystem', 'subsystem'])
