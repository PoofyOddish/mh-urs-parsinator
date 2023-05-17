import tabula
from gql import gql
import utility as util
import table_parse_utility as tp_util
import numpy as np

###
#To Do
# -- Instances where Total Served phrase wraps causes chaos. Need to fix
# -- Appropriateness + outcomes tables are problematic - will circle back
# -- Translate some of the demographic categories so they're used consistently
# -- Access domain sometimes skips first row - need to adjust
# -- Check if a record already exists in db

###
# Define values
state = "Alabama"
year = "2021"
url = "https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf"

# Pull requested PDF
df = tabula.read_pdf(f"./data/{year}/{state}{year}.pdf", pages="all")

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
    ,"Served in Community"
    ,"Served in State Psychiatric Hospitals"
    ,"Number Served"
]

#Outcome
outcome_tables = [
    "Employed as Percent of those in Labor"
    ,"Employed as a % of"
]

for d in range(0, len(df)-1):
    try:
        if df[d].columns[0] in noms_tables:
            tp_util.noms_parsing(df[d],state,year)

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

        elif set(access_tables)&set(df[d].iloc[0].index.tolist()):
            table_name = None
            for row in range(4, df[d].shape[0]):
                if table_name is None:
                    print(f'first value: {df[d].iloc[row][1]}')
                    table_name = input("Confirm table name: ")
                
                if df[d].iloc[row][1] is not np.nan and df[d].iloc[row][0] is not np.nan:

                    for elem in range(0,3):
                    
                        metrics = ["Number Served - Medicaid Only"
                                    ,"Number Served - Non-Medicaid Only"
                                    ,"Number Served - Both Medicaid & Other"
                                    ,"Number Served - Total Served with Known Funding Status"]
                        
                        demographic=util.demographic_check(df[d].iloc[row][0])
                        
                        access_test = {
                            "state_name": state,
                            "year": year,
                            "domain": "ACCESS",
                            "table_name": util.sanitize(table_name),
                            "metric_name": util.sanitize(metrics[elem]),
                            "metric_result": util.coerce_float(df[d].iloc[row][elem+1]),
                        }
                        
                        if not demographic:
                            util.assert_model(access_test)
                            print("\n")
                        else:
                            util.assert_model(access_test|demographic,model='ClientMetricExt')
                            print("\n")
        elif set(outcome_tables)&set(df[d].iloc[0].index.tolist()):
            table_name = None
            print(f'first value: {df[d].iloc[row][1]}')
            table_name = input("Confirm table name: ")

            for row in range(3, df[d].shape[0]):

                if df[d].iloc[row][1] is not np.nan and df[d].iloc[row][0] is not np.nan:
                
                    for elem in range(0,4):

                        metrics = ["Employed"
                                ,"Unemployed"
                                ,"In Labor Force"
                                ,"With Known Employment Status"]
                        
                        demographic=util.demographic_check(df[d].iloc[row][0])

                        outcomes_test = {
                                            "state_name": state,
                                            "year": year,
                                            "domain": "OUTCOMES",
                                            "table_name": util.sanitize(table_name),
                                            "metric_name": util.sanitize(metrics[elem]),
                                            "metric_result": util.coerce_float(df[d].iloc[row][elem+1]),
                                        }
                        
                        if not demographic:
                            util.assert_model(outcomes_test)
                            print("\n")
                        else:
                            util.assert_model(outcomes_test|demographic,model='ClientMetricExt')
                            print("\n")

        
        
        else:
            print("Dang\n")
            print(df[d].iloc[0])
            print("\n")
    except:
        print("Something bad happened. Will deal with that later.")
