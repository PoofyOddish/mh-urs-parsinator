import pytest
import utility as util

"""
Tests needed:
-- state_push
"""

## urs_data_get
def test_get_data_invalid_param():
    with pytest.raises(ValueError):
        util.urs_data_get(env='dev',state=23, year="egg") 

def test_get_data_no_data(env='dev',state='InvalidState',year='2023'):
    assert util.urs_data_get(env, state,year) == {util.dev_prod(env)+'metrics':[]}

##Demographic Check tests
def test_demo_check_no_data():
    with pytest.raises(TypeError):
        util.demographic_check()

def test_demo_check_bad_value():
    with pytest.raises(Exception):
        util.demographic_check(val='boop')

def test_demo_check_good_value():
    assert util.demographic_check(val='Female') == {'client-ext':{'gender':'Female'}}

def test_demo_check_aggregate_value():
    assert util.demographic_check(val='Total') == None

##dev/prod tests
def test_dev_prod_dev():
    assert util.dev_prod(env='DEV') == 'dev_'

def test_dev_prod_prod():
    assert util.dev_prod(env='PROD') == ''

def test_dev_prod_invalid():
    with pytest.raises(Exception):
        util.dev_prod(env='invalid')

##test state_send(env:str,payload: dict)
#def test_state_send_success():


##test state push
def test_state_push_duplicate(env='dev',state='Alabama',url='test',year = '2021'):
    assert util.state_push(env,state,url,year) == None

def test_state_push_success(env='dev',state='Alabama',url='test',year = '2021'):
    import random
    assert util.state_push(env,state,url,year=str(random.randint(1, 999))) == None