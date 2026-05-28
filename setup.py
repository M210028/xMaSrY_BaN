from setuptools import setup, find_packages

setup(
    name="xMaSrY_BaN",
    version="1.0.1",
    packages=find_packages(),
    py_modules=["xMaSrY_BaN"],
    install_requires=[
        "requests",
        "pycryptodome",
        "protobuf",
        "cachetools"
    ],
    author="xMaSrY",
    description="Python utility library",
    python_requires=">=3.9",
)