#!/usr/bin/env python

# builtin imports
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

# module import
from services.log import _logger
from widgets.Fields import *
from setup_scripts.ORM_models import Assets

BoldFont = QtGui.QFont()
BoldFont.setBold(True)


class BlankDataPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BlankDataPanel, self).__init__(parent=parent)
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel('Blank Data Panel\nPlease Select Something')
        self.label.setFont(BoldFont)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
