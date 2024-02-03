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
from setup_scripts.ORM_models import Assets

DEFAULT_THUMBNAIL = pathlib.Path(__file__).parents[1].joinpath('icons/default_thumbnail.png').absolute()


def is_valid_url(url: str) -> typing.Union[bool, tuple]:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class AssetEntry(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, asset_object: Assets, local_thumbnail) -> None:
        super(AssetEntry, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()

        self.image = QtWidgets.QLabel()
        if is_valid_url(asset_object.thumbnail):
            data = urllib.urlopen(asset_object.thumbnail).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            pixmap = pixmap.scaledToWidth(240)
            self.image.setPixmap(pixmap)
        else:
            if pathlib.Path(local_thumbnail).exists():
                pixmap = QtGui.QPixmap(local_thumbnail).scaledToWidth(240)
            else:
                pixmap = QtGui.QPixmap(DEFAULT_THUMBNAIL).scaledToWidgth(240)
            self.image.setPixmap(pixmap)

        self.name_label = QtWidgets.QLabel(asset_object.name)

        self.layout.addWidget(self.image)
        self.layout.addWidget(self.name_label)

        self.setLayout(self.layout)
