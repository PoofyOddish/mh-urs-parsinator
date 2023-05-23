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

existing_data = util.urs_data_get(state,year)

# Pull requested PDF
df = tabula.read_pdf(f"./data/{year}/{state}{year}.pdf", pages="1-2") #all
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
            tp_util.noms_parsing(df[d],state,year,[x for x in existing_data['metrics'] if x['domain'] == 'NOMS'])

        elif set(access_tables)&set(df[d].iloc[1].index.tolist()):
            table_name = util.name_table(df[d].iloc[row][1])
            metric_name = input("Confirm metric name: ")

            for row in range(0, df[d].shape[0]):
                if df[d].iloc[row][0] not in ['Demographics']:
                    if df[d].iloc[row][0] is not np.nan and df[d].iloc[row][1] is not np.nan:
                        demographic=util.demographic_check(df[d].iloc[row][0])
                        
                        access_metric = util.compile_base_metric(state,year,"ACCESS",table_name,metric_name,df[d].iloc[row][1])

                        if not demographic:
                            dup_check = util.check_dup(access_metric,[x for x in existing_data['metrics'] if x['domain'] == 'ACCESS'])

                            if not dup_check:
                                util.assert_model(access_metric)
                                print("\n")
                        else:
                            dup_check = util.check_dup(access_metric|demographic,[x for x in existing_data['metrics'] if x['domain'] == 'ACCESS'])

                            if not dup_check:
                                util.assert_model(access_metric|demographic,model='ClientMetricExt')
                                print("\n")

        elif set(access_tables)&set(df[d].iloc[0].index.tolist()):
            table_name = None
            for row in range(4, df[d].shape[0]):
                if table_name is None:
                    table_name = util.name_table(df[d].iloc[row][1])
                
                if df[d].iloc[row][1] is not np.nan and df[d].iloc[row][0] is not np.nan:

                    for elem in range(0,3):
                    
                        metrics = ["Number Served - Medicaid Only"
                                    ,"Number Served - Non-Medicaid Only"
                                    ,"Number Served - Both Medicaid & Other"
                                    ,"Number Served - Total Served with Known Funding Status"]
                        
                        demographic=util.demographic_check(df[d].iloc[row][0])
                        
                        access_metric = util.compile_base_metric(state,year,"ACCESS",table_name,metrics[elem],df[d].iloc[row][elem+1])
                        
                        if not demographic:
                            dup_check = util.check_dup(access_metric,[x for x in existing_data['metrics'] if x['domain'] == 'ACCESS'])

                            if not dup_check:
                                util.assert_model(access_metric)
                                print("\n")
                        else:
                            dup_check = util.check_dup(access_metric|demographic,[x for x in existing_data['metrics'] if x['domain'] == 'ACCESS'])

                            if not dup_check:
                                util.assert_model(access_metric|demographic,model='ClientMetricExt')
                                print("\n")

        elif set(outcome_tables)&set(df[d].iloc[0].index.tolist()):
            table_name = util.name_table(df[d].iloc[row][1])

            for row in range(3, df[d].shape[0]):

                if df[d].iloc[row][1] is not np.nan and df[d].iloc[row][0] is not np.nan:
                
                    for elem in range(0,4):

                        metrics = ["Employed"
                                ,"Unemployed"
                                ,"In Labor Force"
                                ,"With Known Employment Status"]
                        
                        demographic=util.demographic_check(df[d].iloc[row][0])

                        outcomes_metric = util.compile_base_metric(state,year,"OUTCOMES",table_name,metrics[elem],df[d].iloc[row][elem+1])
                        
                        if not demographic:
                            dup_check = util.check_dup(outcomes_metric,[x for x in existing_data['metrics'] if x['domain'] == 'OUTCOMES'])

                            if not dup_check:
                                util.assert_model(outcomes_metric)
                                print("\n")
                        else:
                            dup_check = util.check_dup(outcomes_metric|demographic,[x for x in existing_data['metrics'] if x['domain'] == 'OUTCOMES'])

                            if not dup_check:
                                util.assert_model(outcomes_metric|demographic,model='ClientMetricExt')
                                print("\n")

        else:
            print("Dang\n")
            print(df[d].iloc[0])
            print("\n")
    except Exception as e:
        print("Something bad happened. Will deal with that later.")
        print(e)
