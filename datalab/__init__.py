"""
"DataLab v0.1.0b2 - Beta Pre-release: structured dirty data diagnosis, Polars + backend optimization, and enhanced data visualization."
"""
__version__ = '0.1.0b2'

import importlib

_subpackages = ['tabular']

__all__ = []

for package in _subpackages:
    module = importlib.import_module(f'{__name__}.{package}')
    
    for name in getattr(module, '__all__', []):
        alias = f'{package}_{name}' if name in globals() else name
        globals()[alias] = getattr(module, name)
        __all__.append(alias)
