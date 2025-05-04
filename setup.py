import os
import sys

from cx_Freeze import Executable, setup

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, "config"))

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="RegEx.exe",
        icon="./config/reg_exp.ico",
        copyright="Copyright (C) 2025 Dmitriy Pavlov",
    )
]

options = {
    "build_exe": {
        "packages": ["tkinter", "customtkinter", "re", "shutil", "os", "concurrent", "logging"],
        "include_files": [
            CONFIG_DIRECTORY,
        ],
        "excludes": [
            "unittest",
            "html",
            "http",
            "xml",
            "bz2",
            "distutils",
            "pydoc_data",
            "test",
            "wheel",
        ],
        "build_exe": "./build/RegEx",
        "include_msvcr": True,
        "zip_include_packages": ".",
    }
}

setup(
    name="RegEx",
    version="2025.05.04",
    description="RegEx",
    author="Dmitriy Pavlov",
    executables=executables,
    options=options
)

# python setup.py build - create app
# python setup.py bdist_msi - create installer
