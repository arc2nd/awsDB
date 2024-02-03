#!/usr/bin/env python

# builtin imports
import sys
import pathlib
import tempfile

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
import PyQt5.QtWidgets as QtWidgets
import qdarkstyle

# module import
from services.log import _logger
from widgets.Fields import *
from widgets.asset_entry import AssetEntry
from tools import search
from tools import get_catalogs as gc
from config.config import config_obj
import config.utils as utils
from setup_scripts.ORM_models import Assets
from services import s3

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
        self.temp_folder = pathlib.Path(tempfile.gettempdir()).joinpath('Instrumentality').absolute()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.search_field = StringField(parent=None, label='Search:')
        self.catalog = ACComboField(parent=self,
                                    label='Catalog:',
                                    options=self._get_catalogs())

        # results
        self.results_layout = QtWidgets.QHBoxLayout()
        self._load_results(asset_list=search.search_string(search_string='d',
                           asset=True,
                           catalog=False,
                           user=False))

        # test_object = Assets(id=5,
        #                      name='cats_test_image',
        #                      version=1,
        #                      path='Reference/cats_test_image/001/cats_test_image.jpg',
        #                      size=2993962,
        #                      hash='blah',
        #                      thumbnail='tests/cats_test_image.thumb.jpg',
        #                      catalog=1,
        #                      created_by=1,
        #                      created='2023-10-18 16:20:05.499352')
        # self.test_asset = AssetEntry(parent=None,
        #                              asset_object=test_object,
        #                              local_thumbnail=)
        # self.results_layout.addWidget(self.test_asset)


        self.main_layout.addWidget(self.search_field)
        self.main_layout.addWidget(self.catalog)
        self.main_layout.addLayout(self.results_layout)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def _get_catalogs(self) -> typing.List[str]:
        return gc.get_catalogs()

    def _search_asset(self):
        catalog = self.catalog.get_data()
        search_string = self.search_field.get_data()
        return search.search_string(search_string=search_string,
                                    asset=True,
                                    catalog=False,
                                    user=False)

    def _load_results(self, asset_list: typing.List[Assets]):
        # make sure that there is a temp_folder
        if not self.temp_folder.exists():
            pathlib.Path(self.temp_folder).mkdir(mode=0o777, parents=True, exist_ok=True)
        # clear the results_layout
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)
        for this_asset in asset_list:
            # for each catalog make a catalog_folder in the temp_folder
            catalog_name = gc.get_catalog_by_id(id=this_asset.catalog)
            catalog_folder = self.temp_folder.joinpath(catalog_name)
            # for each asset make an asset_folder in the catalog_folder
            asset_folder = catalog_folder.joinpath(this_asset.name)
            # for each asset_folder make a version_folder
            version_folder = asset_folder.joinpath(str(this_asset.version).zfill(3))
            # put the thumbnail in that version folder
            destination_path = version_folder.joinpath(pathlib.PurePath(this_asset.thumbnail).name)
            if not destination_path.exists():
                pathlib.Path(version_folder).mkdir(mode=0o777, parents=True, exist_ok=True)
                local_thumbnail = s3.from_aws(dst_path=destination_path,
                                             file_name=pathlib.PurePath(this_asset.thumbnail).name,
                                             catalog=catalog_name,
                                             asset_name=this_asset.name,
                                             version=this_asset.version)

            new_entry = AssetEntry(parent=None,
                                   asset_object=this_asset,
                                   local_thumbnail=str(destination_path))
            self.results_layout.addWidget(new_entry)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = SearcherWindow()
    window.show()

    # Start the event loop.
    app.exec()
