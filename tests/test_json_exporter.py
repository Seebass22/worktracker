import pytest
import datetime
import json_exporter
from pathlib import Path

test_json_file = Path('test_json_file.json')


@pytest.fixture()
def setup():
    test_json_file.unlink(missing_ok=True)

    exporter = json_exporter.json_exporter(json_file=test_json_file)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    yield exporter, current_date

    test_json_file.unlink(missing_ok=True)


def test_first_export(setup):
    exporter, current_date = setup

    exporter.update_json_file('math', 20)
    expected = f'{{\n    "{current_date}": {{\n        "math": 20\n    }}\n}}'

    with test_json_file.open('r') as f:
        data = f.read()

    assert data == expected, "first write failed"


def test_update_existing_activity(setup):
    exporter, current_date = setup

    exporter.update_json_file('math', 20)
    exporter.update_json_file('math', 20)
    expected = f'{{\n    "{current_date}": {{\n        "math": 40\n    }}\n}}'

    with test_json_file.open('r') as f:
        data = f.read()

    assert data == expected, "updating activity failed"


def test_add_new_activity(setup):
    exporter, current_date = setup

    exporter.update_json_file('math', 20)
    exporter.update_json_file('python', 15)
    expected = f'{{\n    "{current_date}": {{\n        "math": 20,\n        "python": 15\n    }}\n}}'

    with test_json_file.open('r') as f:
        data = f.read()

    assert data == expected, "adding new activity failed"
