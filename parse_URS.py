import tabula
import json
import requests
from gql import gql
import utility as util
import numpy as np

###
#To Do
# -- Instances where Total Served phrase wraps causes chaos. Need to fix



###
# Define values
state = "Alabama"
year = "2021"
url = "https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf"

# Prep outbound state data
state_outbound = json.dumps(
    {
        "fips": util.get_fips(state),
        "state_name": state.title(),
        "url": url,
        "year": int(year),
    }
)

# Pull requested PDF
df = tabula.read_pdf(f"./data/{year}/{state}{year}.pdf", pages="all")

# Domain Routing
domains = {"NOMS": "BaseMetric", "Access": "ClientMetricExt"}

# NOMS
noms_tables = [
    "Utilization Rates/Number of Consumers Served",
    "Adult Employment Status",
    "Adult Consumer Survey Measures",
    "Child/Family Consumer Survey Measures",
    'Readmission Rates:(Civil "non-Forensic" clients)',
    "Living Situation",
    "Adult EBP Services",
    "Child/Adolescent EBP Services",
    "Change in Social Connectedness",
]

# Access
access_tables = [
    "Total Served"
]

for d in range(0, len(df)):
    if df[d].columns[0] in noms_tables:
        for elem in list(
            set(df[d].iloc[0].index.tolist())
            & set(["State", "State Number", "State Rate"])):
            for row in range(0, df[d].shape[0]):

                test = {
                    "state_name": state,
                    "year": year,
                    "domain": "NOMS",
                    "table_name": util.sanitize(df[d].columns[0]),
                    "metric_name": util.sanitize(df[d].iloc[row][0]),
                    "metric_result": util.coerce_float(df[d].iloc[row].loc[elem]),
                }

                util.assert_model(test, domains["NOMS"])

    elif set(access_tables)&set(df[d].iloc[1].index.tolist()):
        print(f'first value: {df[d].iloc[3][1]}')
        table_name = input("Confirm table name: ")
        metric_name = input("Confirm metric name: ")

        for row in range(0, df[d].shape[0]):
            if df[d].iloc[row][0] not in ['Demographics']:
                if df[d].iloc[row][0] is not np.nan and df[d].iloc[row][1] is not np.nan:
                    demographic=util.demographic_check(df[d].iloc[row][0])
                    access_test = {
                        "state_name": state,
                        "year": year,
                        "domain": "ACCESS",
                        "table_name": util.sanitize(table_name),
                        "metric_name": util.sanitize(metric_name),
                        "metric_result": util.coerce_float(df[d].iloc[row][1]),
                    }

                    if not demographic:
                        util.assert_model(access_test)
                        print("\n")
                    else:
                        util.assert_model(access_test|demographic,model='ClientMetricExt')
                        print("\n")
    
    
    else:
        print("dang")


