from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    

setup(
    name='DataLab',   # the name of library
    version = '0.1.0', 
    packages = find_packages(),
    install_requires = requirements,
    description='DataLab: Unified End to End Data Library for Tabular and Graph data.',
    author = 'Kshitij Sharma',
    python_required = '>=3.13.7'

    )