import tabula
import json
import requests
from gql import gql
import utility as util

# Define values
state = 'Alabama'
year = '2021'
url = 'https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf'

# Prep outbound state data
state_outbound = json.dumps({
    "fips":util.get_fips(state),
    "state_name":state.title(),
    "url":url,
    "year":int(year)
})

# Pull requested PDF
df = tabula.read_pdf(f'./data/{year}/{state}{year}.pdf',pages='all')

# Domain Routing
domains = {
    'NOMS' : 'BaseMetric',
    'Access' : 'ClientMetricExt'
}

#NOMS
noms_tables = [
    'Utilization Rates/Number of Consumers Served'
    ,'Adult Employment Status'
    ,'Adult Consumer Survey Measures'
    ,'Child/Family Consumer Survey Measures'
    ,'Readmission Rates:(Civil "non-Forensic" clients)'
    ,'Living Situation'
    ,'Adult EBP Services'
    ,'Child/Adolescent EBP Services'
    ,'Change in Social Connectedness'
]

if df[0].columns[0] in noms_tables:
    for row in range(0,df[0].shape[0]):
      test = {
        'state_name': state,
        'year': year,
        'domain': 'NOMS',
        'table_name': df[0].columns[0],
        'metric_name': df[0].iloc[row][0],
        'metric_result': df[0].iloc[row].loc['State']
      }

      util.assert_model(test,domains['NOMS'])

else:
    print('dang')