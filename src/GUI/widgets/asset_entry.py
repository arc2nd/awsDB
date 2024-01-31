#!/usr/bin/env python

# builtin imports
import os
import sys
import typing
import urllib
from urllib.parse import urlparse
import logging
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

# module imports
from services.log import _logger


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class AssetEntry(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, name, image_location):
        super(AssetEntry, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()

        self.image = QtWidgets.QLabel()
        if is_valid_url(image_location):
            data = urllib.urlopen(image_location).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            self.image.setPixmap(pixmap)
        else:
            pixmap = QtGui.QPixmap(image_location)

        self.thumb_label = QtWidgets.QLabel(image_location)
        self.name_label = QtWidgets.QLabel(name)

        self.layout.addWidget(self.image)
        self.layout.addWidget(self.thumb_label)
        self.layout.addWidget(self.name_label)

        self.setLayout(self.layout)
