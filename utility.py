import json
from gql import Client,gql
from pandas import DataFrame

def get_fips(state: str) -> str:
    """
    Get FIPS  
    Return state FIPS value based on state name
    
    Arguments
    ------
    state (str): Name of state for which FIPS is being requested
    """

    with open("./data/fips.txt") as fips_file:
        for line in fips_file:
            state_fip = line.strip().split(maxsplit=1)
            if state_fip[1] == state.upper():
                fips_code = state_fip[0]
                return(fips_code)
            else:
                continue 

def prep_call() -> Client:
    from gql.transport.aiohttp import AIOHTTPTransport
    from gql import Client
    import os

    #Hasura headers
    HASURA_URL = str(os.environ.get('HASURA_URL'))
    HASURA_HEADERS = {"X-Hasura-Admin-Secret": str(os.environ.get('HASURA_ADMIN_SECRET'))}

    transport = AIOHTTPTransport(url=HASURA_URL, headers=HASURA_HEADERS)

    client = Client(transport=transport, fetch_schema_from_transport=True)

    return(client)

def assert_model(payload:json, model:str ='BaseMetric'):
    from metadata_schema.MetricSchema import BaseMetric,ClientMetricExt,ServiceMetricExt
    from pydantic import ValidationError

    try:
        if model == 'BaseMetric':
            BaseMetric(**payload)
            metric_send(prep_base_payload(payload))
            
        elif model == 'ClientMetricExt':
            ClientMetricExt(**payload)
            metric_send(prep_client_payload(payload))

        elif model == 'ServiceMetricExt':
            ServiceMetricExt(**payload)
        else:
            return
        
        print("Successful validation!")
        print(payload)
        print("\n")

    except ValidationError:
        print("Failed validation")
        print(payload)
        print("\n")

def state_send(payload: json):
    from gql import gql

    client = prep_call()

    query = gql(
    """
    mutation insert_state {
    insert_state(objects: {fips: "%s", year: %s, url: "%s", state_name: "%s"}) {
        returning {
        fips
        year
        url
        state_name
        }
    }
    }

    """ % (payload['fips_code'],int(payload['year']), payload['url'], payload['state'].title())
    )

    result = client.execute(query)

def prep_base_payload(payload: json):
    from gql import gql

    query = gql(
    """
    mutation insert_base_metrics {
    insert_metrics(objects: {state_name: "%s", year: %s, domain: "%s", table_name: "%s", metric_name: "%s", metric_result: %s}) {
        returning {
        state_name
        year
        domain
        table_name
        metric_name
        metric_result
        }
    }
    }

    """ % (payload['state_name']
           ,int(payload['year'])
            , payload['domain']
            , payload['table_name']
            , payload['metric_name']
            ,payload['metric_result'])
    )

    return(query)

def prep_client_payload(payload: json):
    from gql import gql

    query = gql(
    """
    mutation insert_base_metrics {
    insert_metrics(objects: {state_name: "%s", year: %s, domain: "%s", table_name: "%s", metric_name: "%s", metric_result: %s, %s:"%s"}) {
        returning {
        state_name
        year
        domain
        table_name
        metric_name
        metric_result
        %s
        }
    }
    }

    """ % (payload['state_name']
           ,int(payload['year'])
            , payload['domain']
            , payload['table_name']
            , payload['metric_name']
            ,payload['metric_result']
            ,list(payload['client-ext'].keys())[0]
            ,payload['client-ext'][list(payload['client-ext'].keys())[0]]
            ,list(payload['client-ext'].keys())[0]
            )
    )

    return(query)

def metric_send(query: gql):
    from time import sleep

    client = prep_call()

    #query = prep_base_payload(payload)

    result = client.execute(query)

    sleep(1)

def coerce_float(val: str) -> float:
    """
    Coerce float
    Attempts to convert str value into a float.
    If a % is detected, will convert accordingly.
    
    Arguments
    ------
    val (str): String to be coerced into a float.
    """
        
    if type(val) == str and '%' in val:
        return(float(val.strip('%'))/100)
    
    try:
        return(float(val.replace(',','').replace('-','')))
    except:
        return(None)
    
def sanitize(val: str) -> str:
    """
    Sanitize Strings
    Helper function to clean up strings. Currently only removes double quotes.
    
    Arguments
    ------
    val (str): String value to sanitize
    """

    val = val.replace('"', '')
    return(val)

def demographic_check(val: str) -> tuple:
    """
    Demographics Extension
    Formats categorical demographic information into expected GQL format
    
    Arguments
    ------
    val (str): Demographic value to be converted to GQL format
    """

    # Total Categories
    total_categories = ['Total'
        ,'Age TOTAL'
        ,'Gender TOTAL'
        ,'TOTAL'
    ]

    demo_categories = {
        'age': [
        '0-12'
        ,'13-17'
        ,'18-20'
        ,'21-24'
        ,'25-44'
        ,'45-64'
        ,'65-74'
        ,'75 and over'
        ,'Age Not Available'
        ,'Age Total'
        ,'Age 0-17'
        ,'Age 18-20'
        ,'Age 21-64'
        ,'Age 65+'
        ,'Age 18 to 20'
        ,'Age 21 to 64'
        ,'Age 65 and over'
    ],
    'adult_or_child': [
        'All Persons Served'
        ,'Children under age 18'
        ,'Adults over age 18'
        ,'Children'
        ,'Adults'
        ,'Age NA'
    ],
    'gender' : [
        'Female'
        ,'Male'
        ,'Gender Not Available'
    ],
    'race' : [
        'American Indian/Alaskan Native'
        ,'Asian'
        ,'Black/African American'
        ,'White'
        ,'Multi-Racial'
        ,'Race Not Available'
        ,'More Than One Race'
        ,'Black or African American'
    ],
    'ethnicity' : [
        'Hispanic or Latino Ethnicity'
        ,'Not Hispanic or Latino Ethnicity'
        ,'Ethnicity Not Available'
        ,'Hispanic or Latino'
        ,'Not Hispanic or Latino'
    ],
    'diagnosis' : [
        'Schizophrenia and Related Disorders'
        ,'Bipolar and Mood Disorders'
        ,'Other Psychoses'
        ,'All other Diagnoses'
        ,'No Diagnosis and Deferred Diagnosis'
    ]

    }

    model_ext = {}

    try:
        if val in total_categories:
            return((model_ext,'BaseModel'))
        
        for key,value in demo_categories.items():
            if val in value:
                model_ext['client-ext']={key:val}
                return((model_ext,'ClientMetricExt'))
            
        if 'client-ext' not in model_ext:
            raise Exception(f'Undefined demographic category: {val}')
    except:
        print("Error: ",val)

def setting_check(val: str) -> dict:
    """
    Service Setting Extension
    Formats categorical service settings into expected GQL format
    
    Arguments
    ------
    val (str): Service setting value to be converted to GQL format
    """
        
    # Total Categories
    total_categories = ['Total']

    # Service Setting Categories
    service_settings = [
        'Private Residence'
        ,'Foster Home'
        ,'Residential Care'
        ,'Crisis Residence'
        ,'Residential Treatment Center'
        ,'Institutional Setting'
        ,'Jail (Correctional Facility)'
        ,'Homeless (Shelter)'
        ,'Other'
        ,'Not Available'
        ,'State Hospitals'
        ,'Other Inpatient'
        ,'Residential Treatment Centers'
        ,'Community Progams'
        ,'State Psychiatric Hospitals'
    ]

    try:
        if val in total_categories:
            return(None)
        elif val in service_settings:
            return({'service-ext':{'service_setting':val}})
        else:
            raise Exception(f'Undefined service setting category: {val}')
    except:
        print("Error: ",val)

def state_push(state: str,url: str,year: str) ->  None:
    """
    Push State Info 
    Push info about a state to API
    
    Arguments
    ------
    state (str): State that is being pushed
    url (str): URL to SAMHSA URS page for state/year
    year (str): Year that is being pushed
    """

    import json
    # Prep outbound state data
    state_outbound = json.dumps(
        {
            "fips": get_fips(state),
            "state_name": state.title(),
            "url": url,
            "year": int(year),
        }
    )

    state_send(state_outbound)

def urs_data_get(state: str, year: str) -> DataFrame:
    """
    Get URS Data  
    Return URS data from API for selected State/Year
    
    Arguments
    ------
    state (str): Name of state for which URS is being requested
    year (str): Year for which URS is being requested
    """

    import pandas as pd
    client = prep_call()

    query = gql(
        '''query GetMetrics {
  metrics(where: {state_name: {_eq: "%s"}, year: {_eq: %s}}) {
    ESMI
    SMI_SED
    adult_or_child
    age
    domain
    employment_status
    ethnicity
    gender
    living_situation
    metric_name
    race
    service_location
    service_type
    state_name
    table_name
    metric_result
    diagnosis
    year
  }
}'''  % (str(state),int(year)))

    result = client.execute(query)

    return(result)

    #return(pd.json_normalize(result['metrics']))

def check_dup(payload: dict,getdata: list) -> bool:
    """
    Check for Duplicate 
    Check to see if payload already exists in API data
    
    Arguments
    ------
    payload (dict): Data set to be pushed to API
    getdata (list): URS dataset for requested state/year
    """

    cols = ['ESMI', 'SMI_SED', 'adult_or_child', 'age'
            , 'employment_status', 'ethnicity', 'gender'
            , 'living_situation', 'race', 'service_location'
            , 'service_type', 'diagnosis','year']
    
    for col in cols:
        if col == 'year':
            payload[col] = int(payload[col])
        else:
            payload.setdefault(col)

    if payload in getdata:
        print("Duplicate record")
        return True #duplicate data
    else:
        print("Unique record")
        return False #not duplicate data
    
def name_table(first_val) -> str:
    print(f'first value: {first_val}')
    table_name = input("Confirm table name: ")
    return(table_name)

def compile_base_metric(state,year,domain,table_name,metric_name,metric_result) -> dict:
    metric_dict = {
        "state_name": state,
        "year": year,
        "domain": domain,
        "table_name": sanitize(table_name),
        "metric_name": sanitize(metric_name),
        "metric_result": coerce_float(metric_result),
        }
    
    return(metric_dict)
