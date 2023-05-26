def urs_parsinator(env: str , state: str, year: str,url: str,page_range:str = 'all') -> None:
    import tabula
    import utility as util
    import table_parse_utility as tp_util
    import numpy as np

    #Add state/year to state table
    util.state_push(env, state,url,year)
    
    #Pull existing data from hasura
    existing_data = util.urs_data_get(env,state,year)

    # Pull requested PDF
    df = tabula.read_pdf(f"./data/{year}/{state}{year}.pdf", pages=page_range) #all

    # Tables
    domain_tables = {
        'NOMS': [
            "Utilization Rates/Number of Consumers Served",
            "Adult Employment Status",
            "Adult Consumer Survey Measures",
            "Child/Family Consumer Survey Measures",
            'Readmission Rates:(Civil "non-Forensic" clients)',
            "Living Situation",
            "Adult EBP Services",
            "Child/Adolescent EBP Services",
            "Change in Social Connectedness",
        ],
        'ACCESS': [
            "Total Served"
            ,"Served in Community"
            ,"Served in State Psychiatric Hospitals"
            ,"Number Served"
        ],
        'OUTCOMES': [
            "Employed as Percent of those in Labor"
            ,"Employed as a % of"
        ]
    }

    for d in range(0, len(df)-1):
        try:
            if df[d].columns[0] in domain_tables['NOMS']:
                tp_util.noms_parsing(env,df[d],state,year,[x for x in existing_data[util.dev_prod(env)+'metrics'] if x['domain'] == 'NOMS'])

            elif set(domain_tables['NOMS'])&set(df[d].iloc[1].index.tolist()):
                table_name = util.name_table(df[d].iloc[row][1])
                metric_name = input("Confirm metric name: ")

                for row in range(0, df[d].shape[0]):
                    if df[d].iloc[row][0] not in ['Demographics']:
                        if df[d].iloc[row][0] is not np.nan and df[d].iloc[row][1] is not np.nan:
                            demographic=util.demographic_check(df[d].iloc[row][0])
                            
                            access_metric = util.compile_base_metric(state,year,"ACCESS",table_name,metric_name,df[d].iloc[row][1])

                            dup_check = util.check_dup(access_metric,[x for x in existing_data[util.dev_prod(env)+'metrics'] if x['domain'] == 'ACCESS'])

                            if not dup_check:
                                util.assert_model(env,access_metric|demographic[0],demographic[1])
                                print("\n")

            elif set(domain_tables['ACCESS'])&set(df[d].iloc[0].index.tolist()):
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
                            
                            dup_check = util.check_dup(access_metric,[x for x in existing_data[util.dev_prod(env)+'metrics'] if x['domain'] == 'ACCESS'])

                            if not dup_check:
                                util.assert_model(env,access_metric|demographic[0],demographic[1])
                                print("\n")

            elif set(domain_tables['OUTCOMES'])&set(df[d].iloc[0].index.tolist()):
                table_name = util.name_table(df[d].iloc[row][1])

                for row in range(3, df[d].shape[0]):

                    if df[d].iloc[row][1] is not np.nan and df[d].iloc[row][0] is not np.nan:
                    
                        for elem in range(0,4):

                            metrics = ["Employed"
                                    ,"Unemployed"
                                    ,"In Labor Force"
                                    ,"With Known Employment Status"]

                            outcomes_metric = util.compile_base_metric(state,year,"OUTCOMES",table_name,metrics[elem],df[d].iloc[row][elem+1])
                            
                            demographic=util.demographic_check(df[d].iloc[row][0])

                            dup_check = util.check_dup(outcomes_metric,[x for x in existing_data[util.dev_prod(env)+'metrics'] if x['domain'] == 'OUTCOMES'])

                            if not dup_check:
                                util.assert_model(env,outcomes_metric|demographic[0],demographic[1])
                                print("\n")

            else:
                print("Dang\n")
                print(df[d].iloc[0])
                print("\n")
        except Exception as e:
            print("Something bad happened. Will deal with that later.")
            print(e)

urs_parsinator('prod',
               "Alabama",
               "2021",
               "https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf",
               "1-3")