from __future__ import print_function

import distutils.spawn
import os
import re
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "semi_labelme/__init__.py"
    with open(filename) as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_install_requires():
    PY3 = sys.version_info[0] == 3
    PY2 = sys.version_info[0] == 2
    assert PY3 or PY2

    install_requires = [
        "imgviz>=0.11,<1.3",
        "matplotlib<3.3",  # for PyInstaller
        "numpy",
        "Pillow>=2.8",
        "PyYAML",
        "qtpy",
        "termcolor",
        "torch==1.9.0",
        "torchvision==0.10.0",
        "imantics",
    ]

    # Find python binding for qt with priority:
    # PyQt5 -> PySide2 -> PyQt4,
    # and PyQt5 is automatically installed on Python3.
    QT_BINDING = None

    try:
        import PyQt5  # NOQA

        QT_BINDING = "pyqt5"
    except ImportError:
        pass

    if QT_BINDING is None:
        try:
            import PySide2  # NOQA

            QT_BINDING = "pyside2"
        except ImportError:
            pass

    if QT_BINDING is None:
        try:
            import PyQt4  # NOQA

            QT_BINDING = "pyqt4"
        except ImportError:
            if PY2:
                print(
                    "Please install PyQt5, PySide2 or PyQt4 for Python2.\n"
                    "Note that PyQt5 can be installed via pip for Python3.",
                    file=sys.stderr,
                )
                sys.exit(1)
            assert PY3
            # PyQt5 can be installed via pip for Python3
            # 5.15.3, 5.15.4 won't work with PyInstaller
            install_requires.append("PyQt5!=5.15.3,!=5.15.4")
            QT_BINDING = "pyqt5"
    del QT_BINDING

    if os.name == "nt":  # Windows
        install_requires.append("colorama")

    return install_requires

def main():
    version = get_version()
    
    setup(
        name="semi_labelme",
        version=version,
        packages=find_packages(),
        description="Annotation Tool Labelme Embedded With Deep Learning",
        author="Shenglin Wang",
        author_email="wongsinglam24@gmail.com",
        url="https://github.com/wongsinglam",
        install_requires=get_install_requires(),
        license="GPLv3",
        keywords="Image Annotation, Deep Learning",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
        ],
        package_data={"semi_labelme": ["icons/*", "config/*.yaml"]},
        entry_points={
            "console_scripts": [
                "semi_labelme=semi_labelme.__main__:main",
                "semi_labelme_draw_json=semi_labelme.cli.draw_json:main",
                "semi_labelme_draw_label_png=semi_labelme.cli.draw_label_png:main",
                "semi_labelme_json_to_dataset=semi_labelme.cli.json_to_dataset:main",
                "semi_labelme_on_docker=semi_labelme.cli.on_docker:main",
            ],
        },
    )


if __name__ == "__main__":
    main()
