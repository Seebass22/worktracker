test:
	python -m pytest

flake8:
	flake8 *.py

exe:
	pyinstaller worktracker.py -y
