#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
import sys, os

setup(
    name='universalmutator',
    version='1.0.16',
    description='Universal regexp-based mutation tool',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=['universalmutator',],
    include_package_data = True,
    package_data = {
        'universalmutator': [
            'static/universal.rules',
            'static/c_like.rules',
            'static/c.rules',
            'static/cpp.rules',
            'static/swift.rules',
            'static/java.rules',
            'static/javascript.rules',
            'static/python.rules',
            'static/rust.rules',
            'static/go.rules',                        
            'static/rust.rules',
            'static/solidity.rules',
            'static/vyper.rules',
            'static/none.rules',
            'static/fe.rules',
            'comby/universal.rules',
            'comby/c_like.rules',
            'comby/c.rules',
            'comby/cpp.rules',
            'comby/swift.rules',
            'comby/java.rules',
            'comby/python.rules',
            'comby/rust.rules',
            'comby/go.rules',                        
            'comby/rust.rules',
            'comby/solidity.rules',
            'comby/vyper.rules',
            'comby/none.rules',
            ]
    },
    license='MIT',
    entry_points="""
    [console_scripts]
    mutate = universalmutator.genmutants:main
    analyze_mutants = universalmutator.analyze:main
    check_covered = universalmutator.checkcov:main
    prioritize_mutants = universalmutator.prioritize:main
    show_mutants = universalmutator.show:main
    prune_mutants = universalmutator.prune:main
    intersect_mutants = universalmutator.intersect:main
    mutant_server = universalmutator.server:main
    """,
    keywords='testing mutation mutation-testing',
    classifiers=[
      "Intended Audience :: Developers",
      "Development Status :: 4 - Beta",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",      
      ],
    install_requires=[
        "comby",
        "python-levenshtein"
    ],
    url='https://github.com/agroce/universalmutator',
)
