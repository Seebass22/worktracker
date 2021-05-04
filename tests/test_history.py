import pytest
import os
import history

TEST_TO_TIME_STRING_DATA = [
        (15, '15s'),
        (66, '1m 6s'),
        (1800, '30m'),
        (3635, '1h 0m 35s'),
]


@pytest.mark.parametrize('seconds,expected', TEST_TO_TIME_STRING_DATA)
def test_to_time_string(seconds, expected):
    result = history.to_time_string(seconds)
    assert result == expected


def test_no_history_file():
    result = history.summarize_day('nonexistant_file.json', '2021-05-04')
    expected = 'no history file'
    assert result == expected


def test_valid_test_json_file():
    test_json_file = 'test_valid_json_file.json'
    with open(test_json_file, 'w') as f:
        f.write('{\n    "2021-05-03": {\n        "math": 25,\n        "python": 20\n    }\n}\n')

    result = history.summarize_day(test_json_file, '2021-05-03')

    expected = 'math: 25s\npython: 20s\n\ntotal: 45s'
    assert result == expected

    if os.path.exists(test_json_file):
        os.remove(test_json_file)


def test_invalid_test_json_file():
    test_json_file = 'test_invalid_json_file.json'
    with open(test_json_file, 'w') as f:
        f.write('{\n    "2021-05-03": {\n        "math": 25\n        "python": 20\n    }\n}\n')

    result = history.summarize_day(test_json_file, '2021-05-03')

    expected = 'invalid json file'
    assert result == expected

    if os.path.exists(test_json_file):
        os.remove(test_json_file)
