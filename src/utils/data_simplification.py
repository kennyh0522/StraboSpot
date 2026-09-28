def binary_simplification(df):
    """converts a pandas dataframe into binary based off of presence in data

    Args:
        df (pandas.DataFrame): a pandas dataframe of the data that needs to be converted to binary

    Returns:
        pandas.DataFrame: a new dataframe that has now been converted to binary
    """
    df_new = df.copy()
    binary_col_data = {}
    columns_to_drop = []
    
    for col in df.columns:
        
        if col == "project_id":
            continue
        # print(f"Converting {col} to binary")
        binary_col_data[col] = df_new[col].replace('', np.nan).notna().astype(int)
        columns_to_drop.append(col)
            
    df_new = df_new.drop(columns=columns_to_drop)
    
    # Add all new binary columns in one go using pd.concat
    if binary_col_data:
        df_new = pd.concat([df_new, pd.DataFrame(binary_col_data, index=df_new.index)], axis=1)
        
    return df_new