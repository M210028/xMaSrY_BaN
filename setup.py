from setuptools import setup

setup(
    name="xMaSrY_BaN",
    version="1.0.4",
    py_modules=[
        "xMaSrY_BaN",
        "MajorLogin_pb2",
        "MajorLogin_res_pb2",
        "GetLoginData_res_pb2"
    ],
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