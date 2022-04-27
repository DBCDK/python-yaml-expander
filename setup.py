from setuptools import find_packages, setup

setup(
    name='yaml-expander',
    version='0.9',
    packages=['yaml_expander'],
    package_dir={'yaml_expander': 'yaml_expander'},
    options={
        'build_exe': {
            'packages': find_packages(exclude=['tests', 'README.md'])
        }
    },
    scripts=['yaml-env-expander'],
#    requires=['yaml'],
    data_files=[('share/man/man1', ['yaml-env-expander.1'])],
    url='https://github.com/DBCDK/yaml-expander',
    license='gpl3',
    author='DBC',
    author_email='dbc@dbc.dk',
    description="Variable expanding in YAML values",
    long_description="""Designed for easy templating of YAML files.
Useful for configuration for different environments."""
)
