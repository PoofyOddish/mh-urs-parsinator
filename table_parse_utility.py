def noms_parsing(df,state,year) -> None:
    """
    NOMS Table Parsing
    NOMS = National Outcome Measures
    
    Arguments
    ------
    df (dataframe): NOMS Table to parse from a dataframe
    state (str): Name of state for which data is being processed
    year (str): Year for which data is being processed
    """

    import utility as util
    for elem in list(
            set(df.iloc[0].index.tolist())
            & set(["State", "State Number", "State Rate"])):
            for row in range(0, df.shape[0]):

                test = {
                    "state_name": state,
                    "year": year,
                    "domain": "NOMS",
                    "table_name": util.sanitize(df.columns[0]),
                    "metric_name": util.sanitize(df.iloc[row][0]),
                    "metric_result": util.coerce_float(df.iloc[row].loc[elem]),
                }

                util.assert_model(test)