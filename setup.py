#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='satchmo-canada-tax',
    version='0.0.2',
    author='David Caplan',
    url='http://github.com/davecap',
    description = 
        'Django app to manage Canadian taxes in Satchmo'
        'Adapted from the version created by Benoit C. Sirois:'
        'http://bitbucket.org/benoitcsirois/satchmo-canada-tax',

    packages=find_packages(),
    include_package_data=True,
    install_requires = [
        'django==1.2.5',
        'satchmo<=0.9.2',
        ]
)
