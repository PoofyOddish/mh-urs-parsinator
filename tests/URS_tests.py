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

##Demographic Check tests
def test_demo_check_no_data():
    with pytest.raises(TypeError):
        util.demographic_check()

def test_demo_check_bad_value():
    with pytest.raises(Exception):
        util.demographic_check(val='boop')

def test_demo_check_good_value():
    assert util.demographic_check(val='Female') == {'client-ext':{'gender':'Female'}}