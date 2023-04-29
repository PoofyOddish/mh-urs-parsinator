##### Test State schema
from metadata_schema.StateSchema import State

test_state = {
    'id': '01',
    'name': 'Alabama',
    'url': 'https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf',
    'year': '2009'
}

state = State(**test_state)

#Pass
assert state.id == "01"

#Fail
assert state.id == "02"

test_bad_state = {
    'id': 1,
    'name': 'Alabama',
    'url': 'https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf',
    'year':'2009'
}

bad_state = State(**test_bad_state)

#Improper coersion
bad_state.id

##### Test Metric schemas
from metadata_schema.MetricSchema import BaseMetric,ClientMetricExt,ServiceMetricExt

test_client_metric = {
    'state_name': 'Alabama',
    'year': 2009,
    'domain': 'Access',
    'table_name': 'Test',
    'metric_name': 'Test Metric',
    'metric_result': 100,
    'living_situation': 'Private Residence',
    'employment_status': 'Unemployed',
    'SMI_SED': 0,

}

client_metric = ClientMetricExt(**test_client_metric)