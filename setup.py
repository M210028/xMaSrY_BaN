from setuptools import setup, find_packages

setup(
    name="xMaSrY_BaN",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pycryptodome",
        "protobuf",
        "cachetools"
    ],
    author="xMaSrY",
    description="xMaSrY_BaN Library",
    long_description="xMaSrY_BaN Library",
    long_description_content_type="text/plain",
)