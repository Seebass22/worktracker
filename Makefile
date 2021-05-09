PYTHON_DIR = /d/programs/python/

test:
	python -m pytest

flake8:
	flake8 *.py

exe:
	pyinstaller worktracker.py -y
	pyinstaller --windowed --hidden-import PySide6.QtGui -y worktracker_gui.py
	cp -r $(PYTHON_DIR)/Lib/site-packages/PySide6/plugins/{styles,platforms} dist/worktracker_gui/
