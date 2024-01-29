#!/usr/bin/env python

# builtin imports
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
import PyQt5.QtWidgets as QtWidgets
import qdarkstyle

# module imports
from services.log import _logger
from widgets.Fields import *
from tools import submit
from tools import get_catalogs
from config.config import config_obj


VERSION = config_obj.version
SETTINGS = {}

# TODO: make my own dark stylesheet?


class SubmitterWindow(QtWidgets.QMainWindow):
    """
    It's just a window
    """
    def __init__(self) -> None:
        super(SubmitterWindow, self).__init__(parent=None)  # parent=getMayaMainWindow())

        self.settings = SETTINGS
        self.setWindowTitle("Submitter")
        ## Set up status bar
        if 'test' in self.settings:
            msg = 'In test mode'
        else:
            msg = 'Welcome to Submitter - {}'.format(VERSION)
        self.statusBar().showMessage(msg)

        self.main_widget = SubmitterWidget(parent=self)
        self.setCentralWidget(self.main_widget)

    def set_status_msg(self, msg: str = '') -> None:
        self.statusBar().showMessage(msg)


class SubmitterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SubmitterWidget, self).__init__(parent=parent)
        self.parent = parent
        self.main_layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Submitter')
        label.setFont(BoldFont)
        self.asset_name = StringField(parent=self, label='Asset Name:')
        self.asset_path = FileField(label='File Path:')
        self.catalog = ACComboField(parent=self,
                                    label='Catalog:',
                                    options=self._get_catalogs())

        self.submit_button = QtWidgets.QPushButton('Submit')
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.cancel_button)

        self.submit_button.clicked.connect(self._submit_asset)
        self.cancel_button.clicked.connect(self.parent.close)

        self.main_layout.addWidget(label)
        self.main_layout.addWidget(self.asset_name)
        self.main_layout.addWidget(self.asset_path)
        self.main_layout.addWidget(self.catalog)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def _get_catalogs(self) -> typing.List[str]:
        return get_catalogs.get_catalogs()

    def _submit_asset(self) -> None:
        success = True
        asset_name = self.asset_name.get_data()
        asset_path = self.asset_path.get_data()
        catalog = self.catalog.get_data()
        _logger.info(f'submitting asset: {asset_name}')
        print(f'submitting asset: {asset_name}')
        if success:
            self.parent.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = SubmitterWindow()
    window.show()

    # Start the event loop.
    app.exec()
