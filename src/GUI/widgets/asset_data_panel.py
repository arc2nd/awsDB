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
from tools import get_users as gu
import widgets.Fields as Fields
from setup_scripts.ORM_models import Assets

BoldFont = QtGui.QFont()
BoldFont.setBold(True)


def _get_user_by_id(user_id: int) -> str:
    return gu.get_user_by_id(id=user_id)


class AssetDataPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AssetDataPanel, self).__init__(parent=parent)
        self.parent = parent
        self.active = True
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setContentsMargins(0, 0, 0, 0)

        self.name_field = Fields.StringField(label='Name:')
        self.version_field = Fields.StringField(label='Version:')
        self.path_field = Fields.StringField(label='Path:')
        self.src_path_field = Fields.StringField(label='Source Path:')
        self.size_field = Fields.StringField(label='File Size:')
        self.created_field = Fields.StringField(label='Creation Time:')
        self.created_by_field = Fields.StringField(label='Created By:')
        self.view_button = QtWidgets.QPushButton('View...')
        self.download_button = QtWidgets.QPushButton('Download...')

        self.layout.addWidget(self.name_field)
        self.layout.addWidget(self.version_field)
        self.layout.addWidget(self.path_field)
        self.layout.addWidget(self.src_path_field)
        self.layout.addWidget(self.size_field)
        self.layout.addWidget(self.created_field)
        self.layout.addWidget(self.created_by_field)
        self.layout.addWidget(self.view_button)
        self.layout.addWidget(self.download_button)
        self.setLayout(self.layout)

    def load(self, this_asset: Assets) -> None:
        self.active = False
        self.name_field.set_data(this_asset.name)
        self.version_field.set_data(this_asset.version)
        self.path_field.set_data(this_asset.path)
        self.src_path_field.set_data(this_asset.source_path)
        self.size_field.set_data(this_asset.size)
        self.created_field.set_data(this_asset.created)
        self.created_by_field.set_data(_get_user_by_id(this_asset.created_by))
        self.active = True
