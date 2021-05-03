import pytest
import os
import datetime
import json_exporter

test_json_file = 'test_json_file.json'


@pytest.fixture()
def setup():
    if os.path.exists(test_json_file):
        os.remove(test_json_file)

    exporter = json_exporter.json_exporter(json_file=test_json_file)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    yield exporter, current_date

    if os.path.exists(test_json_file):
        os.remove(test_json_file)


def test_first_export(setup):
    exporter, current_date = setup

    exporter.update_json_file('math', 20)
    expected = f'{{\n    "{current_date}": {{\n        "math": 20\n    }}\n}}'

    with open(test_json_file, 'r') as f:
        data = f.read()

    assert data == expected, "first write failed"


def test_update_existing_activity(setup):
    exporter, current_date = setup

    exporter.update_json_file('math', 20)
    exporter.update_json_file('math', 20)
    expected = f'{{\n    "{current_date}": {{\n        "math": 40\n    }}\n}}'

    with open(test_json_file, 'r') as f:
        data = f.read()

    assert data == expected, "updating activity failed"


def test_add_new_activity(setup):
    exporter, current_date = setup

    exporter.update_json_file('math', 20)
    exporter.update_json_file('python', 15)
    expected = f'{{\n    "{current_date}": {{\n        "math": 20,\n        "python": 15\n    }}\n}}'

    with open(test_json_file, 'r') as f:
        data = f.read()

    assert data == expected, "updating activity failed"
