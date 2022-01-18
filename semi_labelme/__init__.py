# flake8: noqa

import logging
import sys

from qtpy import QT_VERSION


__appname__ = "semi_labelme"


__version__ = "0.1.0"

QT4 = QT_VERSION[0] == "4"
QT5 = QT_VERSION[0] == "5"
del QT_VERSION

PY2 = sys.version[0] == "2"
PY3 = sys.version[0] == "3"
del sys

from semi_labelme.label_file import LabelFile
from semi_labelme import testing
from semi_labelme import utils
