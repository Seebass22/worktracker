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

        self.today_button = QtWidgets.QPushButton("time spent today")
        self.toggle_button = QtWidgets.QPushButton("")
        self.text = QtWidgets.QLabel("",
                                     alignment=QtCore.Qt.AlignCenter)
        self.activity = QtWidgets.QLineEdit()
        self.activity.setPlaceholderText("enter activity")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.today_button)
        self.layout.addWidget(self.activity)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.toggle_button)

        self.today_button.clicked.connect(self.today)
        self.toggle_button.clicked.connect(self.toggle_working)

        self.set_button_text()

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
        self.text.setText(ret)

    @QtCore.Slot()
    def stop_tracking(self):
        ret = self.worktracker.stop()
        self.text.setText(ret)

    @QtCore.Slot()
    def today(self):
        ret = history.today(self.worktracker.json_file)
        self.text.setText(ret)

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
