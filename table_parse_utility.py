from pandas import DataFrame
def noms_parsing(df: DataFrame,state: str,year: str, URS_data: list) -> None:
    """
    NOMS Table Parsing
    NOMS = National Outcome Measures
    
    Arguments
    ------
    df (dataframe): NOMS Table to parse from a dataframe
    state (str): Name of state for which data is being processed
    year (str): Year for which data is being processed
    URS_data (list): URS data for NOMS domain for selected state/year
    """

    import utility as util

    for elem in list(
            set(df.iloc[0].index.tolist())
            & set(["State", "State Number", "State Rate"])):
            for row in range(0, df.shape[0]):

                noms_metric = util.compile_base_metric(state,year,"NOMS",df.columns[0],df.iloc[row][0],df.iloc[row].loc[elem])
                
                dup_check = util.check_dup(noms_metric,URS_data)

                if not dup_check:
                    util.assert_model(noms_metric)