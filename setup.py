#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

packages = [
    'dnsproxy',
    'dnsproxy.lib'
]

requires = open("requirements.txt").read().split()

setup(
    name='dnsproxy',
    version='0.0.1',
    description='DNS to DNS-over-TLS Proxy',
    packages=find_packages(),
    package_dir={'dnsproxy': 'dnsproxy'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'dnsproxy = dnsproxy.dnsproxy:main'
        ]
    },
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
