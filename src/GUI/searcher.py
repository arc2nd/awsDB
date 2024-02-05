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
from widgets.blank_data_panel import BlankDataPanel
from widgets.asset_data_panel import AssetDataPanel
from tools import search
from tools import alternate_search as a_search
from tools import get_catalogs as gc
from config.config import config_obj
import config.utils as utils
from setup_scripts.ORM_models import Assets
from services import s3

VERSION = config_obj.version
SETTINGS = {}


# TODO: hook up buttons in asset_data_panel
# TODO: gridlayout the results widgets
# TODO: handle other types of searches (now it's just assets, want to search users,roles,catalogs)
# TODO: make initial results a search for 'latest'

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
            msg = f'Welcome to Searcher - {VERSION}'
        self.statusBar().showMessage(msg)

        self.central_widget = SearcherWidget(parent=self)
        self.setCentralWidget(self.central_widget)

    def set_status_msg(self, msg: str = '') -> None:
        self.statusBar().showMessage(msg)


class SearcherWidget(QtWidgets.QWidget):
    """
    the primary widget that holds all the searcher stuff
    """
    def __init__(self, parent=None):
        super(SearcherWidget, self).__init__(parent=parent)
        self.parent = parent
        self.temp_folder = pathlib.Path(tempfile.gettempdir()).joinpath('Instrumentality').absolute()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.search_layout = QtWidgets.QVBoxLayout()
        self.items_layout = QtWidgets.QHBoxLayout()
        self.results_layout = QtWidgets.QHBoxLayout()

        self.search_field = StringField(parent=None, label='Search:', enter_func=self.line_search)
        self.catalog_field = ACComboField(parent=self,
                                          label='Catalog:',
                                          options=self._get_catalogs())

        self.stack = QtWidgets.QStackedWidget(self)

        self.blank_panel = BlankDataPanel()  # 0
        self.asset_panel = AssetDataPanel()  # 1

        self.stack.setCurrentIndex(0)

        self.stack.addWidget(self.blank_panel)  # 0
        self.stack.addWidget(self.asset_panel)  # 1

        # results
        self._load_results(asset_list=search.search_string(search_string='r',
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

        self.menubar = QtWidgets.QMenuBar(self)
        self.file_menu = self.menubar.addMenu('File')

        self.main_layout.addWidget(self.menubar)

        self.main_layout.addLayout(self.search_layout)
        self.search_layout.addWidget(self.search_field)
        self.search_layout.addWidget(self.catalog_field)
        self.items_layout.addLayout(self.results_layout)
        self.items_layout.addWidget(self.stack)
        self.main_layout.addLayout(self.items_layout)
        self.main_layout.addStretch()

        self._create_file_menu()

        self.setLayout(self.main_layout)

    def line_search(self) -> None:
        """
        the method to run when enter is pressed in the search_field
            resets the stack to a blank_data_panel,
            runs the search
            loads the results of the search into the results_layout

        Returns:
            None
        """
        self.stack.setCurrentIndex(0)
        assets = self._search_asset()
        _logger.debug(f'Asset: {assets}')
        self._load_results(asset_list=assets)

    @staticmethod
    def _get_catalogs() -> typing.List[str]:
        """
        call out to the get_catalogs tool to get a list of all catalog names
        make sure we stick 'All' at the beginning of the list

        Returns:
            catalog_list: List[str]
        """
        catalog_list = ['All']
        db_catalogs = gc.get_catalogs()
        catalog_list.extend(db_catalogs)
        return catalog_list

    def _search_asset(self) -> typing.List[Assets]:
        """
        get the data form the catalog_field and the search_field and
        run the search.

        Returns:
            List[Assets]
        """
        catalog = self.catalog_field.get_data()
        search_string = self.search_field.get_data()
        # return search.search_string(search_string=search_string,
        #                               asset=True,
        #                               catalog=catalog,
        #                               user=False)
        return a_search.search_string(search_string=search_string,
                                    asset=True,
                                    catalog=catalog,
                                    user=False)['assets']

    def _load_results(self, asset_list: typing.List[Assets]):
        """
        load all the assets objects form the search into the results_layout
        this is done by attempting to download the thumbnail from storage,
        creating an AssetEntry object for each by using it's data

        Args:
            asset_list: List[Assets]

        Returns:
            None
        """
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
            new_entry.clicked.connect(self._clicked_asset)
            self.results_layout.addWidget(new_entry)

    def _clicked_asset(self, event):
        """
        What to do when you click on one of the AssetEntry widgets in the results_layout
        Args:
            event:

        Returns:
            None
        """
        _logger.debug(f'Clicked Asset: {event}')
        self.stack.setCurrentIndex(1)
        self.asset_panel.load(event)


    def _create_file_menu(self) -> None:
        """
        Create the 'File' menu

        Args:
            None
        Returns:
            None
        """
        line_search_action = QtWidgets.QAction('Search', self)
        line_search_action.setStatusTip('Search')
        line_search_action.triggered.connect(self.line_search)

        self.file_menu.addAction(line_search_action)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = SearcherWindow()
    window.show()

    # Start the event loop.
    app.exec()
