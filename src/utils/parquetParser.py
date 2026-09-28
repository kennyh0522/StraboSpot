import pandas as pd
import pyarrow.parquet as pq
import glob
from sys import getsizeof 

def parquet_parser(folder_name):
    print("Running...")
    
    # Parquet files
    parquet_files = glob.glob(folder_name)
    print(len(parquet_files))

    # List to store DataFrames
    dfs = []
    memory = 0

    # Read each Parquet file and convert it to a Pandas DataFrame
    for file in parquet_files:

        table = pq.read_table(file)
        df = table.to_pandas()  # Convert PyArrow Table to Pandas DataFrame
        dfs.append(df)
        memory += getsizeof(df)
        if memory > 1E9:
            # dfs takes a gigabyte of memory
            break

    # Concatenate all DataFrames into one large DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    # Verify the result by inspecting the first few rows
    combined_df.info(verbose=True)

    return combined_df