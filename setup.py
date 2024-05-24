#!/usr/bin/env python

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(name="pyu",
          version="0.1.1",
          description="Python utilities for common tasks",
          author="PyU Team",
          author_email="posh.bc@gmail.com",
          install_requires=["PyYAML==6.0.1"],
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
          ],
          url="https://github.com/poshjosh/pyu",
          packages=find_packages(
              where='src',
              include=['pyu'],
          ),
          package_dir={"": "src"},
          )
