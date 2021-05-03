import pytest
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
