import pytest
import utility as util

"""
Tests needed:
-- urs_data_get(state: str, year: str): no data returned
"""


def test_get_data_invalid_param():
    with pytest.raises(ValueError):
        util.urs_data_get(state=23, year="egg") 

def test_get_data_no_data():
    assert util.urs_data_get(state="InvalidState", year="2023") == {'metrics':[]}