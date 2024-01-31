#!/usr/bin/env python

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

import os
import sys
import typing
import logging
import pathlib
_logger = logging.getLogger('awsDB_Submitter')

from functools import wraps
import time

def timer(f):
    @wraps(f)
    def wrapper_time(*args, **kwargs):
        start_time = time.perf_counter()
        value = f(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        _logger.info('func: {} took {}s'.format(f.__name__, run_time))
        return value
    return wrapper_time


BoldFont = QtGui.QFont()
BoldFont.setBold(True)


# FileField Widget wrapper
class FileField(QtWidgets.QWidget):
    def __init__(self, parent=None, label: str = ''):
        super(FileField, self).__init__(parent)
        self.name = label
        self.parent = parent

        # Widgets
        self.main_row = QtWidgets.QVBoxLayout()
        self.main_row.setSpacing(0)
        self.main_row.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(label)
        self.label.setFont(BoldFont)
        self.line_row = QtWidgets.QHBoxLayout()
        self.line = QtWidgets.QLineEdit()
        self.btn = QtWidgets.QPushButton('...')
        self.btn.setMaximumWidth(25)

        self.line_row.addWidget(self.line)
        self.line_row.addWidget(self.btn)

        self.main_row.addWidget(self.label)
        self.main_row.addLayout(self.line_row)

        self.btn.clicked.connect(self.open_file)

        self.setLayout(self.main_row)

    def get_data(self):
        return {self.label.text(): self.line.text()}

    def set_data(self, data: str):
        self.line.setText(data)

    def open_file(self):
        filename = QtWidgets.QFileDialog().getOpenFileName(self, 'Pick {} File'.format(self.name))[0]
        # dirname = str(QtWidgets.QFileDialog().getExistingDirectory(self, 'Select Directory'))
        abs_file = os.path.abspath(filename)
        self.line.setText(abs_file)


class StringField(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QLayout, label: str, enter_func=None) -> None:
        super(StringField, self).__init__()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(label)
        self.label.setFont(BoldFont)
        self.field = QtWidgets.QLineEdit()
        self.enabled = True

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.field)
        self.setLayout(self.layout)

    def get_data(self) -> str:
        return self.field.text()

    def set_data(self, value: str) -> None:
        return self.field.setText(str(value))

    def set_enabled(self, value: bool) -> None:
        self.field.setEnabled(value)
        self.enabled = value


class ACComboField(QtWidgets.QWidget):
    def __init__(self, parent, label: str, options: typing.List[str]) -> None:
        super(ACComboField, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(label)
        self.label.setFont(BoldFont)
        self.combo = QtWidgets.QComboBox()
        for opt in options:
            self.combo.addItem(opt)

        self.combo_completer = QtWidgets.QCompleter(options)
        self.combo_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.combo.setEditable(True)
        self.combo.setCompleter(self.combo_completer)
        self.combo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.setLayout(self.layout)

    def get_data(self) -> str:
        return self.combo.currentText()

    def get_index_data(self, index: int) -> str:
        return self.combo.itemText(index)

    def set_data(self, input: str) -> None:
        return self.combo.setCurrentText(input)

    def set_options(self, options: typing.List[str]) -> None:
        self.combo.clear()
        self.combo_completer = QtWidgets.QCompleter(options)
        self.combo_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.combo.setCompleter(self.combo_completer)
        for opt in options:
            self.combo.addItem(opt)

    def set_enabled(self, value: bool) -> None:
        self.field.setEnabled(value)

    def set_placeholder(self, value: str) -> None:
        self.field.setPlaceholderText(value)
