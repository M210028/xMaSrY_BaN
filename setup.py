from setuptools import setup, find_packages

setup(
    name="xMaSrY_BaN",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pycryptodome",
        "protobuf",
        "cachetools"
    ],
)