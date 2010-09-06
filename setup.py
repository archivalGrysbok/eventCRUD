#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='eventCRUD',
    version= '0.8.0.4.7.8',
    description='LARP event management for the Django web framework',
    author='Stacy Haponik',
    author_email='stacy.haponik@gmail.com',
    url='http://github.com/cincrin/eventCRUD',
    packages=find_packages(),

    include_package_data=True,
    zip_safe=False,
)
