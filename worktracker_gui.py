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

        self.layout = QtWidgets.QVBoxLayout(self)
        self.tracking_tab = QtWidgets.QWidget()
        self.history_tab = QtWidgets.QWidget()

        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(self.tracking_tab, "tracking")
        tabwidget.addTab(self.history_tab, "history")
        self.layout.addWidget(tabwidget)

        self.setup_tracking_tab()
        self.setup_history_tab()

        # signals
        self.today_button.clicked.connect(self.today)
        self.yesterday_button.clicked.connect(self.yesterday)
        self.toggle_button.clicked.connect(self.toggle_working)
        self.days_ago_button.clicked.connect(self.days_ago_f)
        self.date_button.clicked.connect(self.date_f)

        self.set_button_text()

    def setup_tracking_tab(self):
        self.toggle_button = QtWidgets.QPushButton("")
        self.status_text = QtWidgets.QLabel("")
        self.activity = QtWidgets.QLineEdit()
        self.activity.setPlaceholderText("enter activity")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.activity)
        layout.addWidget(self.status_text)
        layout.addWidget(self.toggle_button)
        self.tracking_tab.setLayout(layout)

    def setup_history_tab(self):
        self.today_button = QtWidgets.QPushButton("today")
        self.yesterday_button = QtWidgets.QPushButton("yesterday")
        self.history_text = QtWidgets.QLabel("")

        # days ago
        self.days_ago_input = QtWidgets.QLineEdit()
        self.days_ago_input.setPlaceholderText("days ago")
        self.days_ago_button = QtWidgets.QPushButton("go")

        self.days_ago = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.days_ago_input)
        hbox.addWidget(self.days_ago_button)
        self.days_ago.setLayout(hbox)

        # date
        self.date_input = QtWidgets.QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.date_button = QtWidgets.QPushButton("go")

        self.date = QtWidgets.QWidget()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.date_input)
        hbox2.addWidget(self.date_button)
        self.date.setLayout(hbox2)

        # populate tab
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.today_button)
        layout.addWidget(self.yesterday_button)
        layout.addWidget(self.days_ago)
        layout.addWidget(self.date)
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
    def days_ago_f(self):
        days_text = self.days_ago_input.text()
        try:
            days = int(days_text)
            ret = history.days_ago(self.worktracker.json_file, days)
            self.history_text.setText(ret)
        except ValueError:
            self.history_text.setText("not a number...")

    @QtCore.Slot()
    def date_f(self):
        date_string = self.date_input.text()
        ret = history.summarize_day(self.worktracker.json_file, date_string)
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
    widget.resize(300, 300)
    widget.show()

    sys.exit(app.exec_())
