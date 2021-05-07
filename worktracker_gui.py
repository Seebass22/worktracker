import sys
from PySide6 import QtCore, QtWidgets
from pathlib import Path

from worktracker import worktracker
import history


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        json_file = Path('gui_history.json')
        status_file = Path('gui_status.txt')

        self.worktracker = worktracker(status_file, json_file)

        self.today_button = QtWidgets.QPushButton("time spent today")
        self.start_button = QtWidgets.QPushButton("start tracking")
        self.stop_button = QtWidgets.QPushButton("stop tracking")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        self.activity = QtWidgets.QLineEdit()
        self.activity.setPlaceholderText("enter activity")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.today_button)
        self.layout.addWidget(self.activity)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.today_button.clicked.connect(self.today)
        self.start_button.clicked.connect(self.start_tracking)
        self.stop_button.clicked.connect(self.stop_tracking)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec_())
