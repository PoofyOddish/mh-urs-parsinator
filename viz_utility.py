from pandas import DataFrame

def viz_data_get(domain: str = None) -> DataFrame:
    """
    Get URS Data  
    Return URS data from API for selected State/Year
    
    Arguments
    ------
    env (str): Indicates if data should be pushed to PROD or DEV db
    state (str): Name of state for which URS is being requested
    year (str): Year for which URS is being requested
    """

    import pandas as pd
    import utility as util
    from gql import gql

    client = util.prep_call()

    query = gql(
        '''query GetMetrics {
    metrics(where: {domain: {_eq: "%s"}}) {
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
}'''  % (domain))

    result = client.execute(query)

    return(pd.DataFrame.from_dict(result['metrics']))