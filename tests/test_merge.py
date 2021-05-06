import pytest
from pathlib import Path
import json
import merge


@pytest.fixture()
def setup():
    valid_old_file = Path('test_valid_old_file.json')
    valid_new_file = Path('test_valid_new_file.json')

    with valid_old_file.open('w') as f:
        f.write('{"2021-05-06": {"python": 25, "math": 35}}')

    with valid_new_file.open('w') as f:
        f.write('{"2021-05-06": {"python": 10, "piano": 20}}')

    yield valid_old_file, valid_new_file

    valid_old_file.unlink()
    valid_new_file.unlink()


def test_merge(setup):
    test_old_file, test_new_file = setup

    merge.merge_json(test_old_file, test_new_file)

    with test_old_file.open('r') as f:
        result = json.load(f)

    expected = dict()
    expected['2021-05-06'] = {'python': 35, 'math': 35, 'piano': 20}

    assert result == expected


def test_merge_no_new_file(setup):
    # old file untouched
    test_old_file, _ = setup
    test_new_file = Path('missing_file.json')

    with test_old_file.open('r') as f:
        expected = f.read()

    merge.merge_json(test_old_file, test_new_file)

    with test_old_file.open('r') as f:
        result = f.read()

    assert result == expected


def test_merge_invalid_new_json(setup):
    # old file untouched
    test_old_file, _ = setup
    test_new_file = Path('test_invalid_json_file.json')

    with test_new_file.open('w') as f:
        f.write('{"2021-05-06": {"python": 25, "math": 35,}}')

    with test_old_file.open('r') as f:
        expected = f.read()

    merge.merge_json(test_old_file, test_new_file)

    with test_old_file.open('r') as f:
        result = f.read()

    assert result == expected

    test_new_file.unlink()
