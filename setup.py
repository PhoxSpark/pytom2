"""
Python setup
"""
from __future__ import absolute_import
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="pytomproject",
    version="0.4.3",
    author="Luis Gracia",
    author_email="luisgracia@phoxspark.com",
    description="BSC Python Practice for Bioinformatics.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/PhoxSpark/pytom-project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
