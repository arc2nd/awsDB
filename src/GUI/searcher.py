#!/usr/bin/env python

# builtin imports
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
import PyQt5.QtWidgets as QtWidgets
import qdarkstyle

# module import
from services.log import _logger
from widgets.Fields import *
from widgets.asset_entry import AssetEntry
from tools import search
from tools import get_catalogs
from config.config import config_obj
import config.utils as utils

VERSION = config_obj.version
SETTINGS = {}


class SearcherWindow(QtWidgets.QMainWindow):
    """
    It's just a window
    """
    def __init__(self) -> None:
        super(SearcherWindow, self).__init__(parent=None)  # parent=getMayaMainWindow())

        self.settings = SETTINGS
        self.setWindowTitle("Searcher")
        ## Set up status bar
        if 'test' in self.settings:
            msg = 'In test mode'
        else:
            msg = 'Welcome to Searcher - {}'.format(VERSION)
        self.statusBar().showMessage(msg)

        self.main_widget = SearcherWidget(parent=self)
        self.setCentralWidget(self.main_widget)

    def set_status_msg(self, msg: str = '') -> None:
        self.statusBar().showMessage(msg)


class SearcherWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SearcherWidget, self).__init__(parent=parent)
        self.parent = parent
        self.main_layout = QtWidgets.QVBoxLayout()

        self.search_field = StringField(parent=None, label='Search:')
        self.catalog = ACComboField(parent=self,
                                    label='Catalog:',
                                    options=self._get_catalogs())

        # results
        self.results_layout = QtWidgets.QHBoxLayout()
        self._load_results(asset_list=search.search_string(search_string='r',
                           asset=True,
                           catalog=False,
                           user=False))

        self.search_button = QtWidgets.QPushButton('Search')
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.search_button)
        self.button_layout.addWidget(self.cancel_button)

        self.search_button.clicked.connect(self._search_asset)
        self.cancel_button.clicked.connect(self.parent.close)

        self.main_layout.addWidget(self.search_field)
        self.main_layout.addWidget(self.catalog)
        self.main_layout.addLayout(self.results_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def _get_catalogs(self) -> typing.List[str]:
        return get_catalogs.get_catalogs()

    def _search_asset(self):
        catalog = self.catalog.get_data()
        search_string = self.search_field.get_data()
        return search.search_string(search_string=search_string,
                                    asset=True,
                                    catalog=False,
                                    user=False)

    def _load_results(self, asset_list: typing.List[dict]):
        # clear the results_layout
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)
        for this_asset in asset_list:
           # asset_obj = utils.dict2obj(this_asset)
            new_entry = AssetEntry(parent=None,
                                   name=this_asset.name,
                                   image_location=this_asset.thumbnail)
            self.results_layout.addWidget(new_entry)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = SearcherWindow()
    window.show()

    # Start the event loop.
    app.exec()
