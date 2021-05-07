#!/usr/bin/python
import sys
from PySide6 import QtCore, QtWidgets
from pathlib import Path

import worktracker
import history


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.worktracker = worktracker.worktracker()

        self.toggle_button = QtWidgets.QPushButton("")
        self.status_text = QtWidgets.QLabel("")
        self.activity = QtWidgets.QLineEdit()
        self.activity.setPlaceholderText("enter activity")

        self.today_button = QtWidgets.QPushButton("time spent today")
        self.yesterday_button = QtWidgets.QPushButton("time spent yesterday")
        self.history_text = QtWidgets.QLabel("")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.tracking_tab = QtWidgets.QWidget()
        self.history_tab = QtWidgets.QWidget()

        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(self.tracking_tab, "tracking")
        tabwidget.addTab(self.history_tab, "history")
        self.layout.addWidget(tabwidget)

        self.setup_tracking_tab()
        self.setup_history_tab()

        self.today_button.clicked.connect(self.today)
        self.yesterday_button.clicked.connect(self.yesterday)
        self.toggle_button.clicked.connect(self.toggle_working)

        self.set_button_text()

    def setup_tracking_tab(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.activity)
        layout.addWidget(self.status_text)
        layout.addWidget(self.toggle_button)
        self.tracking_tab.setLayout(layout)

    def setup_history_tab(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.today_button)
        layout.addWidget(self.yesterday_button)
        layout.addWidget(self.history_text)
        self.history_tab.setLayout(layout)


    def is_working(self):
        time, _ = self.worktracker.get_status()
        if time is None:
            return False
        else:
            return True

    def set_button_text(self):
        if self.is_working():
            self.toggle_button.setText("stop")
        else:
            self.toggle_button.setText("start")

    @QtCore.Slot()
    def start_tracking(self):
        activity = self.activity.text()
        ret = self.worktracker.start(activity)
        self.status_text.setText(ret)

    @QtCore.Slot()
    def stop_tracking(self):
        ret = self.worktracker.stop()
        self.status_text.setText(ret)

    @QtCore.Slot()
    def today(self):
        ret = history.today(self.worktracker.json_file)
        self.history_text.setText(ret)

    @QtCore.Slot()
    def yesterday(self):
        ret = history.yesterday(self.worktracker.json_file)
        self.history_text.setText(ret)

    @QtCore.Slot()
    def toggle_working(self):
        if self.is_working():
            self.stop_tracking()
        else:
            self.start_tracking()

        self.set_button_text()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec_())
