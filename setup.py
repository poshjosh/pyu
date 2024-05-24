#!/usr/bin/env python

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(name="pyu",
          version="0.1.0",
          packages=find_packages(
              where='src',
              include=['pyu'],
          ),
          package_dir={"": "src"},
          install_requires=["PyYAML==6.0.1"],
          )
